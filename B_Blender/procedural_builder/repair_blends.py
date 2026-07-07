"""
repair_blends.py — Make already-exported station .blend files open fast.

The station files are geometrically light (~17k tris), but they were saved with
3D viewports that draw materials in EEVEE. On the first Material-Preview /
Rendered draw EEVEE compiles a GLSL shader per material, blocking Blender's main
thread for many seconds (minutes on weak GPUs) — the file appears to "not open".

This script opens each .blend, forces every saved 3D viewport to Solid shading
and a valid render engine, then resaves. No geometry is touched. Run headless:

    blender --background --python repair_blends.py
    blender --background --python repair_blends.py -- <file1.blend> <file2.blend>
"""

import os
import sys
import glob

try:
    import bpy
except ImportError:  # pragma: no cover
    bpy = None

_HERE = os.path.dirname(os.path.abspath(__file__))
_BLEND_DIR = os.path.join(os.path.dirname(_HERE), "exports", "blend")


def _valid_engine():
    ids = [e.identifier for e in
           bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    for cand in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        if cand in ids:
            return cand
    return ids[0] if ids else None


def _force_solid():
    n = 0
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = "SOLID"
                    space.shading.color_type = "MATERIAL"
                    n += 1
    return n


def repair(path):
    bpy.ops.wm.open_mainfile(filepath=path)
    engine = _valid_engine()
    if engine:
        bpy.context.scene.render.engine = engine
    viewports = _force_solid()
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    print("[repair] %s  (viewports->solid: %d, engine: %s)"
          % (os.path.basename(path), viewports, engine))


def main():
    if "--" in sys.argv:
        files = sys.argv[sys.argv.index("--") + 1:]
    else:
        files = sorted(glob.glob(os.path.join(_BLEND_DIR, "*.blend")))
    if not files:
        print("[repair] no .blend files found in", _BLEND_DIR)
        return
    for f in files:
        if os.path.exists(f):
            repair(f)
        else:
            print("[repair] missing:", f)
    print("[repair] done:", len(files), "file(s)")


if __name__ == "__main__":
    main()
