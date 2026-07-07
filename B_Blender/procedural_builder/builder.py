"""
builder.py — Single generic entry point for the procedural station renderer.

    build_station(parameter_file, assembly_file, constraints_file, rules_file)

Consumes four JSON specifications and produces a Blender scene, a .blend, a .glb
and a review screenshot. The code contains no station names and no geometry
numbers — every dimension, name, material and build step comes from the JSON.

Run headless (auto-discovers specs in ../parametric_specs when no args given):

    blender --background --python builder.py
    blender --background --python builder.py -- <params> <assembly> <constraints> <rules>
"""

import os
import sys
import json
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
_B_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, os.path.join(_B_ROOT, "generators")):
    if _p not in sys.path:
        sys.path.append(_p)

import geometry_builder as gb          # noqa: E402
import component_registry as registry  # noqa: E402
import validation as valid             # noqa: E402
from scene_builder import SceneBuilder  # noqa: E402
from assembly_engine import apply_hierarchy  # noqa: E402

try:
    import bpy  # noqa: E402
    import common_blender_utils as cbu  # noqa: E402
    _HAS_BPY = True
except ImportError:
    bpy = None
    cbu = None
    _HAS_BPY = False


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _review_scene(root):
    """Generic floor patch + lighting + camera framing whatever was built.

    Uses only station-agnostic infrastructure helpers; no station knowledge.
    """
    cx, cy, _ = root.location
    # Neutral floor patch under the station (review only).
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy + 1.0, -0.05))
    floor = bpy.context.active_object
    floor.name = "PHYS_Review_FloorPatch"
    floor.scale = (8.0, 9.0, 0.1)

    cbu.setup_lighting()
    cam = cbu.setup_camera(location=(cx + 2.6, cy + 5.4, 3.3), focal_length=35.0)
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(cx, cy, 1.1))
    target = bpy.context.active_object
    target.name = "CAM_Target"
    con = cam.constraints.new(type="TRACK_TO")
    con.target = target
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"


def _pick_eevee_engine():
    """Return the EEVEE engine identifier valid for this Blender build.

    The identifier changed across versions (``BLENDER_EEVEE_NEXT`` in 4.2-4.x,
    ``BLENDER_EEVEE`` again in 5.x). Setting a non-existent id raises TypeError
    and silently leaves the engine unset, so resolve it from the live enum.
    """
    try:
        ids = [e.identifier for e in
               bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    except Exception:  # noqa: BLE001
        return None
    for cand in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        if cand in ids:
            return cand
    return None


def _open_in_solid_shading():
    """Force every saved 3D viewport to Solid shading so the file opens fast.

    The station materials are simple, but EEVEE compiles a GLSL shader per
    material on the first Material-Preview / Rendered draw, which blocks
    Blender's main thread for many seconds (minutes on weak GPUs) — the file
    then "won't open". Saving in Solid shading skips that stall entirely; the
    user opts into materials by switching shading when ready.
    """
    try:
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type != "VIEW_3D":
                    continue
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.shading.type = "SOLID"
                        space.shading.color_type = "MATERIAL"
    except Exception as exc:  # noqa: BLE001
        print("[builder] could not set solid shading:", exc)


def _render_png(path):
    try:
        scene = bpy.context.scene
        engine = _pick_eevee_engine()
        if engine:
            scene.render.engine = engine
        scene.render.resolution_x = 1280
        scene.render.resolution_y = 720
        scene.render.image_settings.file_format = "PNG"
        cbu.ensure_dir(path)
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        return os.path.exists(path)
    except Exception as exc:  # noqa: BLE001
        print("[builder] screenshot skipped:", exc)
        return False


def build_station(parameter_file, assembly_file, constraints_file, rules_file,
                  export=True, out_basename=None):
    """Build one station from its four specification files. Returns a Report."""
    if not _HAS_BPY:
        raise RuntimeError("build_station() must run inside Blender.")

    params = _load(parameter_file)
    assembly = _load(assembly_file)
    constraints = _load(constraints_file) if constraints_file else {}
    rules = _load(rules_file) if rules_file else {}

    # --- static validation before building ---
    report = valid.validate_specs(params, assembly,
                                  known_types=registry.known_types())

    cbu.clear_scene()
    cbu.set_units_to_meters()

    # --- build geometry from parameters ---
    sb = SceneBuilder(params, rules)
    objects, root = sb.build()

    # --- resolve hierarchy from assembly ---
    for w in apply_hierarchy(assembly.get("operations", []), objects):
        report.warning("assembly", w)
    for w in sb.ctx.warnings + sb.mat.warnings:
        report.warning("build", w)

    # --- runtime validation after building ---
    valid.validate_built(objects, constraints, report)

    # --- review scene + export ---
    _review_scene(root)

    if out_basename is None:
        base = os.path.basename(parameter_file)
        out_basename = base.replace("_parameters.json", "").replace(".json", "")

    if export:
        blend = os.path.join(_B_ROOT, "exports", "blend", out_basename + ".blend")
        glb = os.path.join(_B_ROOT, "exports", "glb", out_basename + ".glb")
        png = os.path.join(_B_ROOT, "exports", "screenshots", out_basename + ".png")
        _open_in_solid_shading()
        cbu.save_blend(blend)
        cbu.export_glb(glb)
        shot = _render_png(png)
        print("[builder] blend :", blend)
        print("[builder] glb   :", glb)
        print("[builder] png   :", png if shot else "(not created)")

    print("[builder] objects built:", len(objects))
    print("[builder] validation   :", report.summary())
    for issue in report.issues:
        print("   ", issue)
    return report


# ---------------------------------------------------------------------------
# CLI / discovery
# ---------------------------------------------------------------------------

def _discover(specs_dir):
    params = sorted(glob.glob(os.path.join(specs_dir, "*_parameters.json")))
    out = []
    for p in params:
        a = p.replace("_parameters.json", "_assembly.json")
        if os.path.exists(a):
            out.append((p, a))
    return out


def _cli_args():
    if "--" in sys.argv:
        return sys.argv[sys.argv.index("--") + 1:]
    return []


def main():
    specs_dir = os.path.join(_B_ROOT, "parametric_specs")
    constraints = os.path.join(specs_dir, "manufacturing_constraints.json")
    rules = os.path.join(specs_dir, "industrial_rules.json")

    args = _cli_args()
    if len(args) >= 2:
        pairs = [(args[0], args[1])]
        if len(args) >= 4:
            constraints, rules = args[2], args[3]
    else:
        pairs = _discover(specs_dir)
        if not pairs:
            print("[builder] no *_parameters.json / *_assembly.json pairs found in",
                  specs_dir)
            return

    for params_file, assembly_file in pairs:
        print("=" * 60)
        print("[builder] building from:", os.path.basename(params_file))
        build_station(params_file, assembly_file, constraints, rules)


if __name__ == "__main__":
    main()
