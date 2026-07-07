"""
DEPRECATED — kept as a fallback / reference only.

This station-specific generator is superseded by the generic, JSON-driven
`procedural_builder/` pipeline (build S01 from `parametric_specs/loading_station_*`
via `procedural_builder/builder.py`). It is retained for reference and as a
fallback; prefer the procedural builder for all new work. Do not extend this file.

generate_loading_station.py — VEKIFAB WP B station generator (S01, Loading Station).

Generates ONLY station S01 (the Loading Station) as a lightweight but visually
industrial module, driven by requirements/factory_description.json and built
entirely from the helpers in common_blender_utils.py.

Contents built:
  * Industrial loading table (with legs) + a stack of boxes
  * Pallet zone floor marking + 2 pallets
  * Short output conveyor connecting to the next station (S02)
  * Safety floor markings, a control panel and an emergency-stop button
  * Info panel facing the avatar walkway + an info trigger zone

Everything is placed into a collection named STATION_01_Loading and parented to a
STATION_01_Loading_Root empty, with Unity-friendly names and custom properties
(collider / rigidbody / trigger tags) for the Unity import.

Run headless:
    blender --background --python generate_loading_station.py

Outputs:
    exports/blend/01_loading_station.blend
    exports/glb/01_loading_station.glb
    exports/screenshots/01_loading_station.png   (best effort)

This script only builds S01 — it does NOT build the full factory and does NOT
modify any JSON file.
"""

import os
import sys
import math

# Make sure this script's directory is importable so we can load the utils.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.append(_HERE)

import bpy  # noqa: E402  (only available inside Blender)
import common_blender_utils as cbu  # noqa: E402

_B_ROOT = os.path.dirname(_HERE)  # .../B_Blender
_REQ_DIR = os.path.join(_B_ROOT, "requirements")
_FACTORY_JSON = os.path.join(_REQ_DIR, "factory_description.json")
_LIBRARY_JSON = os.path.join(_REQ_DIR, "station_library.json")

STATION_ID = "S01"
COLLECTION_NAME = "STATION_01_Loading"


# ---------------------------------------------------------------------------
# Small local helpers
# ---------------------------------------------------------------------------

def _activate_new_collection(name):
    """Create a collection, link it to the scene and make it the active target
    so every object created afterwards is placed inside it."""
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    layer_coll = bpy.context.view_layer.layer_collection.children[coll.name]
    bpy.context.view_layer.active_layer_collection = layer_coll
    return coll


def _parent_keep(child, parent):
    """Parent `child` to `parent` while preserving its current world transform."""
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()


def _find(seq, **kv):
    """Return the first dict in `seq` matching all key/value pairs (or None)."""
    for item in seq:
        if all(item.get(k) == v for k, v in kv.items()):
            return item
    return None


def _aim_camera_at(cam_obj, target_location):
    """Point a camera at a world location using a tracked empty target."""
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=target_location)
    target = bpy.context.active_object
    target.name = "CAM_Target_Loading"
    con = cam_obj.constraints.new(type="TRACK_TO")
    con.target = target
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    return target


# ---------------------------------------------------------------------------
# Station builder
# ---------------------------------------------------------------------------

def build_loading_station():
    """Build the S01 Loading Station and return (root_empty, collection)."""
    factory = cbu.load_json(_FACTORY_JSON)
    library = cbu.load_json(_LIBRARY_JSON)

    station = _find(factory["stations"], id=STATION_ID)
    if station is None:
        raise RuntimeError("Station S01 not found in factory_description.json")
    conveyor = _find(factory["conveyors"], **{"from": STATION_ID}) or {}
    info = _find(factory["info_panels"], station=STATION_ID) or {}
    template = library["station_types"].get(station["type"], {})

    px, py, _pz = station["position"]

    def P(dx, dy, z):
        """Position relative to the station centre (station rotation is 0)."""
        return (px + dx, py + dy, z)

    # --- Materials ---------------------------------------------------------
    mats = cbu.create_default_materials()
    mats["cardboard"] = cbu.create_material(
        "MAT_Cardboard", (0.58, 0.42, 0.26, 1.0), metallic=0.0, roughness=0.85)
    mats["wood_pallet"] = cbu.create_material(
        "MAT_WoodPallet", (0.55, 0.40, 0.24, 1.0), metallic=0.0, roughness=0.75)

    # --- Collection + station root ----------------------------------------
    coll = _activate_new_collection(COLLECTION_NAME)

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(px, py, 0.0))
    root = bpy.context.active_object
    root.name = "STATION_01_Loading_Root"
    cbu.add_custom_property(root, "unity_tag", "Station")
    cbu.add_custom_property(root, "station_id", STATION_ID)
    cbu.add_custom_property(root, "station_type", station["type"])
    for i, tag in enumerate(template.get("unity_tags", [])):
        cbu.add_custom_property(root, "unity_tag_%d" % i, tag)

    top_level = []  # objects to parent to root at the end

    # --- Industrial loading table -----------------------------------------
    table = cbu.create_cube(
        "COLLIDER_Loading_Table", location=P(-0.3, -0.6, 0.90),
        scale=(1.6, 0.8, 0.08), material=mats["metal_light"])
    cbu.add_bevel_modifier(table, amount=0.02)
    cbu.mark_static_collider(table)
    cbu.add_custom_property(table, "unity_tag", "Table")

    leg_offsets = [(-1.00, -0.90), (0.40, -0.90), (-1.00, -0.30), (0.40, -0.30)]
    for i, (lx, ly) in enumerate(leg_offsets, start=1):
        leg = cbu.create_cube(
            "STATION_01_Loading_TableLeg_%d" % i,
            location=P(lx, ly, 0.43), scale=(0.08, 0.08, 0.86),
            material=mats["metal_dark"])
        cbu.mark_static_collider(leg)
        _parent_keep(leg, table)
    top_level.append(table)

    # --- Stack of boxes on the table (rigidbody candidates) ---------------
    box_size = 0.34
    table_top_z = 0.90 + 0.04  # table centre z + half thickness
    box_grid = [(-0.55, -0.75), (-0.15, -0.75), (-0.55, -0.40), (-0.15, -0.40)]
    box_index = 0
    for layer in range(2):  # two layers -> 8 boxes total (within 6..10)
        z = table_top_z + box_size / 2.0 + layer * box_size
        # Offset the upper layer slightly for a stacked-pallet look.
        jitter = 0.03 if layer else 0.0
        for gx, gy in box_grid:
            box_index += 1
            box = cbu.create_cube(
                "PHYS_Loading_Box_%d" % box_index,
                location=P(gx + jitter, gy - jitter, z),
                scale=(box_size, box_size, box_size),
                material=mats["cardboard"])
            cbu.add_bevel_modifier(box, amount=0.01)
            cbu.mark_rigidbody(box, mass=0.5, kinematic=False)
            cbu.add_custom_property(box, "unity_tag", "Box")
            top_level.append(box)

    # --- Pallet zone floor marking + 2 pallets ----------------------------
    zone = cbu.create_warning_floor_marking(
        "STATION_01_Loading_PalletZone", location=P(0.05, 0.60, 0.0),
        scale=(1.9, 1.3), materials=mats)
    cbu.mark_static_collider(zone)
    top_level.append(zone)

    for i, dx in enumerate((-0.45, 0.50), start=1):
        pallet = cbu.create_cube(
            "STATION_01_Loading_Pallet_%d" % i,
            location=P(dx, 0.55, 0.06), scale=(0.9, 0.75, 0.12),
            material=mats["wood_pallet"])
        cbu.mark_static_collider(pallet)
        cbu.add_custom_property(pallet, "unity_tag", "Pallet")
        top_level.append(pallet)

    # --- Short output conveyor to the next station ------------------------
    c_start = conveyor.get("start", [px + 1.0, py, 0.4])
    c_end = conveyor.get("end", [px + 2.25, py, 0.4])
    conv = cbu.create_simple_conveyor(
        "CONVEYOR_Loading_Output", start=c_start, end=c_end,
        width=conveyor.get("width_m", 0.6),
        height=conveyor.get("height_m", 0.4), materials=mats)
    # Requirement: treat this segment as a static collider candidate.
    cbu.mark_static_collider(conv)
    cbu.add_custom_property(conv, "unity_tag", "Conveyor")
    cbu.add_custom_property(conv, "connects_to", conveyor.get("to", "S02"))
    top_level.append(conv)

    # --- Safety floor markings (walkway-edge stripe) ----------------------
    stripe = cbu.create_warning_floor_marking(
        "STATION_01_Loading_SafetyStripe", location=P(0.0, 1.4, 0.0),
        scale=(2.0, 0.15), materials=mats)
    cbu.mark_static_collider(stripe)
    top_level.append(stripe)

    # --- Control panel + emergency stop -----------------------------------
    panel = cbu.create_control_panel(
        "STATION_01_Loading_ControlPanel", location=P(-1.30, -0.55, 1.05),
        materials=mats)
    cbu.mark_static_collider(panel)
    top_level.append(panel)

    estop = cbu.create_emergency_stop(
        "STATION_01_Loading_EStop", location=P(-1.30, -0.88, 1.20),
        materials=mats)
    top_level.append(estop)

    # --- Info panel facing the avatar walkway (+Y) ------------------------
    ip_pos = info.get("position", [px, py + 2.6, 1.6])
    ip_text = info.get("text", "Loading Station")
    # cbu places the panel text on its local -Y face; rotate 180 deg so it
    # faces +Y toward the walkway.
    info_panel = cbu.create_info_panel(
        "INFO_Loading_Panel", title="Loading Station", body=ip_text,
        location=tuple(ip_pos), rotation=(0, 0, math.radians(180)),
        materials=mats)
    top_level.append(info_panel)

    # --- Info trigger zone (in front of the panel) ------------------------
    trigger = cbu.create_trigger_zone(
        "TRIGGER_Info_Loading",
        location=(ip_pos[0], ip_pos[1] + 0.7, 1.1),
        scale=(2.2, 1.6, 2.2))
    cbu.add_custom_property(trigger, "station_id", STATION_ID)
    top_level.append(trigger)

    # --- Parent everything to the station root ----------------------------
    for obj in top_level:
        _parent_keep(obj, root)

    return root, coll


# ---------------------------------------------------------------------------
# Review scene: floor, lighting, camera, screenshot
# ---------------------------------------------------------------------------

def setup_review_scene(station_center):
    """Add a small floor patch, lighting and a camera framing the station."""
    # A small floor patch under the station (not the whole 25x18 factory).
    mats = cbu.create_default_materials()
    cx, cy = station_center
    floor = cbu.create_cube(
        "PHYS_Loading_FloorPatch",
        location=(cx, cy + 1.0, -0.05), scale=(6.0, 8.0, 0.1),
        material=mats["white_panel"])
    cbu.add_custom_property(floor, "unity_tag", "Floor")
    cbu.mark_static_collider(floor)

    cbu.setup_lighting()

    cam = cbu.setup_camera(location=(cx + 2.4, cy + 5.2, 3.2), focal_length=35.0)
    _aim_camera_at(cam, (cx, cy, 1.1))
    return cam


def render_screenshot(path):
    """Render a single still to `path`. Best effort — never fatal."""
    try:
        scene = bpy.context.scene
        try:
            scene.render.engine = "BLENDER_EEVEE_NEXT"
        except (TypeError, AttributeError):
            pass  # keep whatever engine is default on this Blender build
        scene.render.resolution_x = 1280
        scene.render.resolution_y = 720
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = "PNG"
        cbu.ensure_dir(path)
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        return os.path.exists(path)
    except Exception as exc:  # noqa: BLE001 — screenshot is optional
        print("[loading] screenshot skipped:", exc)
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cbu.clear_scene()
    cbu.set_units_to_meters()

    root, _coll = build_loading_station()
    station_center = (root.location.x, root.location.y)
    setup_review_scene(station_center)

    blend_path = os.path.join(_B_ROOT, "exports", "blend", "01_loading_station.blend")
    glb_path = os.path.join(_B_ROOT, "exports", "glb", "01_loading_station.glb")
    png_path = os.path.join(_B_ROOT, "exports", "screenshots", "01_loading_station.png")

    cbu.save_blend(blend_path)
    cbu.export_glb(glb_path)
    shot_ok = render_screenshot(png_path)

    print("[loading] saved blend :", blend_path)
    print("[loading] exported glb:", glb_path)
    print("[loading] screenshot  :", png_path if shot_ok else "(not created)")


if __name__ == "__main__":
    main()
