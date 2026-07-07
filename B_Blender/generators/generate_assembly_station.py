"""
generate_assembly_station.py — VEKIFAB WP B station generator (S02, Assisted Assembly).

Generates ONLY station S02 (the Assisted Assembly Station) as a lightweight but
visually detailed industrial module, driven by requirements/factory_description.json
and built entirely from the helpers in common_blender_utils.py.

Deliberately different from the Loading Station: a cabinet-style workbench with a
pegboard tool rack, angled small-parts bins, an assembly fixture holding
semi-assembled pump mock-ups, an HMI monitor on a pole, and an overhead task
light.

Contents built:
  * Industrial workbench (worktop + cabinet base with drawers)
  * Pegboard tool rack with hanging tools
  * Row of angled small-parts bins
  * Semi-assembled compact infusion-pump mock-ups (rigidbody candidates)
  * Assembly fixture / jig
  * Overhead task light (fixture + real light)
  * HMI control screen on a stand
  * Operator standing-zone floor marking
  * Input + output conveyor stubs (from factory_description.json)
  * Info panel facing the avatar walkway + an info trigger zone

Run headless:
    blender --background --python generate_assembly_station.py

Outputs:
    exports/blend/02_assembly_station.blend
    exports/glb/02_assembly_station.glb
    exports/screenshots/02_assembly_station.png   (best effort)

This script only builds S02 — it does NOT build the full factory and does NOT
modify any JSON file.
"""

import os
import sys
import math

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.append(_HERE)

import bpy  # noqa: E402  (only available inside Blender)
import common_blender_utils as cbu  # noqa: E402

_B_ROOT = os.path.dirname(_HERE)
_REQ_DIR = os.path.join(_B_ROOT, "requirements")
_FACTORY_JSON = os.path.join(_REQ_DIR, "factory_description.json")
_LIBRARY_JSON = os.path.join(_REQ_DIR, "station_library.json")

STATION_ID = "S02"
COLLECTION_NAME = "STATION_02_Assembly"


# ---------------------------------------------------------------------------
# Small local helpers (shared shape with generate_loading_station.py)
# ---------------------------------------------------------------------------

def _activate_new_collection(name):
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    layer_coll = bpy.context.view_layer.layer_collection.children[coll.name]
    bpy.context.view_layer.active_layer_collection = layer_coll
    return coll


def _parent_keep(child, parent):
    """Parent while preserving world transform."""
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()


def _find(seq, **kv):
    for item in seq:
        if all(item.get(k) == v for k, v in kv.items()):
            return item
    return None


def _aim_camera_at(cam_obj, target_location):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=target_location)
    target = bpy.context.active_object
    target.name = "CAM_Target_Assembly"
    con = cam_obj.constraints.new(type="TRACK_TO")
    con.target = target
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    return target


def _build_pump(name, location, mats, semi=False):
    """Build a small compact-infusion-pump mock-up and return its body object.

    Args:
        name: Object name (should start with 'PHYS_Assembly_Part_').
        location: World-space centre of the pump body.
        mats: Default-materials dict.
        semi: If True, build a semi-assembled unit (open, no display fitted).

    Returns:
        The pump body object (screen/knob parented, marked as a rigidbody).
    """
    x, y, z = location
    body = cbu.create_cube(name, location=location,
                           scale=(0.12, 0.08, 0.045), material=mats["white_panel"])
    cbu.add_bevel_modifier(body, amount=0.008)
    cbu.shade_smooth(body)

    if not semi:
        # Fitted front display (+Y face).
        screen = cbu.create_cube(name + "_Screen",
                                 location=(x, y - 0.041, z + 0.006),
                                 scale=(0.06, 0.005, 0.025),
                                 material=mats["screen_dark"])
        _parent_keep(screen, body)
    # Small delivery knob / roller on top.
    knob = cbu.create_cylinder(name + "_Knob", location=(x + 0.035, y, z + 0.03),
                               radius=0.012, depth=0.02,
                               material=mats["blue_accent"], vertices=12)
    cbu.shade_smooth(knob)
    _parent_keep(knob, body)

    cbu.mark_rigidbody(body, mass=0.3, kinematic=False)
    cbu.add_custom_property(body, "unity_tag", "PumpPart")
    cbu.add_custom_property(body, "assembly_state", "semi" if semi else "assembled")
    return body


# ---------------------------------------------------------------------------
# Station builder
# ---------------------------------------------------------------------------

def build_assembly_station():
    """Build the S02 Assisted Assembly Station; return (root_empty, collection)."""
    factory = cbu.load_json(_FACTORY_JSON)
    library = cbu.load_json(_LIBRARY_JSON)

    station = _find(factory["stations"], id=STATION_ID)
    if station is None:
        raise RuntimeError("Station S02 not found in factory_description.json")
    conv_in = _find(factory["conveyors"], to=STATION_ID) or {}
    conv_out = _find(factory["conveyors"], **{"from": STATION_ID}) or {}
    info = _find(factory["info_panels"], station=STATION_ID) or {}
    template = library["station_types"].get(station["type"], {})

    px, py, _pz = station["position"]

    def P(dx, dy, z):
        return (px + dx, py + dy, z)

    mats = cbu.create_default_materials()

    coll = _activate_new_collection(COLLECTION_NAME)

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(px, py, 0.0))
    root = bpy.context.active_object
    root.name = "STATION_02_Assembly_Root"
    cbu.add_custom_property(root, "unity_tag", "Station")
    cbu.add_custom_property(root, "station_id", STATION_ID)
    cbu.add_custom_property(root, "station_type", station["type"])
    for i, tag in enumerate(template.get("unity_tags", [])):
        cbu.add_custom_property(root, "unity_tag_%d" % i, tag)

    top_level = []

    # --- Workbench: worktop (collider) + cabinet base + drawers ------------
    worktop = cbu.create_cube(
        "COLLIDER_Assembly_Workbench", location=P(0.0, -0.6, 0.90),
        scale=(1.9, 0.75, 0.08), material=mats["metal_dark"])
    cbu.add_bevel_modifier(worktop, amount=0.02)
    cbu.mark_static_collider(worktop)
    cbu.add_custom_property(worktop, "unity_tag", "Workbench")

    cabinet = cbu.create_cube(
        "STATION_02_Assembly_BenchCabinet", location=P(0.0, -0.5, 0.42),
        scale=(1.7, 0.55, 0.84), material=mats["metal_light"])
    cbu.mark_static_collider(cabinet)
    _parent_keep(cabinet, worktop)

    for i, dx in enumerate((-0.55, 0.0, 0.55), start=1):
        # Drawer fronts on the operator (+Y) side.
        drawer = cbu.create_cube(
            "STATION_02_Assembly_Drawer_%d" % i, location=P(dx, -0.23, 0.55),
            scale=(0.5, 0.03, 0.5), material=mats["blue_accent"])
        _parent_keep(drawer, cabinet)
        handle = cbu.create_cube(
            "STATION_02_Assembly_DrawerHandle_%d" % i, location=P(dx, -0.22, 0.65),
            scale=(0.22, 0.03, 0.03), material=mats["metal_dark"])
        _parent_keep(handle, cabinet)

    top_level.append(worktop)

    # --- Pegboard tool rack + hanging tools --------------------------------
    rack = cbu.create_cube(
        "STATION_02_Assembly_ToolRack", location=P(0.0, -0.98, 1.45),
        scale=(1.6, 0.04, 0.9), material=mats["blue_accent"])
    cbu.mark_static_collider(rack)
    for i, (tx, tz, th) in enumerate(
            [(-0.6, 1.45, 0.28), (-0.3, 1.5, 0.20), (0.25, 1.45, 0.30),
             (0.6, 1.5, 0.18)], start=1):
        tool = cbu.create_cube(
            "STATION_02_Assembly_Tool_%d" % i, location=P(tx, -0.94, tz),
            scale=(0.035, 0.035, th), material=mats["metal_dark"])
        _parent_keep(tool, rack)
    top_level.append(rack)

    # --- Angled small-parts bins on the worktop back edge ------------------
    bin_mats = [mats["blue_accent"], mats["safety_yellow"], mats["white_panel"],
                mats["blue_accent"]]
    for i, dx in enumerate((-0.7, -0.4, -0.1, 0.2), start=1):
        b = cbu.create_cube(
            "STATION_02_Assembly_Bin_%d" % i, location=P(dx, -0.78, 1.00),
            scale=(0.22, 0.16, 0.12), material=bin_mats[i - 1])
        b.rotation_euler = (math.radians(-18), 0, 0)  # tilt toward operator
        cbu.mark_static_collider(b)
        _parent_keep(b, worktop)

    # --- Assembly fixture / jig on the worktop -----------------------------
    fixture = cbu.create_cube(
        "STATION_02_Assembly_Fixture", location=P(-0.35, -0.45, 0.97),
        scale=(0.34, 0.28, 0.05), material=mats["metal_dark"])
    cbu.add_bevel_modifier(fixture, amount=0.01)
    cbu.mark_static_collider(fixture)
    for i, (cx, cy) in enumerate([(-0.5, -0.45), (-0.2, -0.45)], start=1):
        post = cbu.create_cylinder(
            "STATION_02_Assembly_FixturePost_%d" % i, location=P(cx, cy, 1.03),
            radius=0.015, depth=0.10, material=mats["metal_light"], vertices=10)
        _parent_keep(post, fixture)
    _parent_keep(fixture, worktop)

    # --- Semi-assembled pump mock-ups (rigidbody candidates) ---------------
    pumps = [
        ("PHYS_Assembly_Part_1", P(-0.35, -0.45, 1.02), False),  # in the fixture
        ("PHYS_Assembly_Part_2", P(0.35, -0.55, 0.99), True),    # semi, on bench
        ("PHYS_Assembly_Part_3", P(0.55, -0.30, 0.99), False),
        ("PHYS_Assembly_Part_4", P(-0.65, -0.30, 0.99), True),
    ]
    for name, loc, semi in pumps:
        pump = _build_pump(name, loc, mats, semi=semi)
        top_level.append(pump)

    # --- HMI control screen on a pole --------------------------------------
    hmi_pole = cbu.create_cylinder(
        "STATION_02_Assembly_HMIPole", location=P(0.85, -0.55, 0.55),
        radius=0.04, depth=1.10, material=mats["metal_dark"], vertices=12)
    hmi_screen = cbu.create_cube(
        "STATION_02_Assembly_HMI", location=P(0.85, -0.47, 1.35),
        scale=(0.4, 0.03, 0.3), material=mats["screen_dark"])
    hmi_screen.rotation_euler = (math.radians(-12), 0, 0)  # tilt toward operator
    cbu.mark_static_collider(hmi_screen)
    cbu.add_custom_property(hmi_screen, "unity_tag", "HMI")
    _parent_keep(hmi_pole, hmi_screen)
    top_level.append(hmi_screen)

    # --- Overhead task light (fixture + real light) ------------------------
    fixture_light = cbu.create_cube(
        "STATION_02_Assembly_TaskLight", location=P(0.0, -0.5, 2.20),
        scale=(1.2, 0.18, 0.06), material=mats["metal_light"])
    cbu.add_custom_property(fixture_light, "unity_tag", "TaskLight")
    top_level.append(fixture_light)

    light_data = bpy.data.lights.new("LIGHT_Assembly_Task", type="AREA")
    light_data.energy = 120.0
    light_data.size = 1.0
    light_obj = bpy.data.objects.new("LIGHT_Assembly_Task", light_data)
    light_obj.location = P(0.0, -0.5, 2.12)
    bpy.context.collection.objects.link(light_obj)
    _parent_keep(light_obj, fixture_light)

    # --- Operator standing-zone floor marking ------------------------------
    zone = cbu.create_warning_floor_marking(
        "STATION_02_Assembly_OperatorZone", location=P(0.0, 0.45, 0.0),
        scale=(1.5, 0.8), materials=mats)
    cbu.mark_static_collider(zone)
    top_level.append(zone)

    # --- Input + output conveyor stubs -------------------------------------
    if conv_in:
        c_in = cbu.create_simple_conveyor(
            "CONVEYOR_Assembly_Input", start=conv_in["start"], end=conv_in["end"],
            width=conv_in.get("width_m", 0.6), height=conv_in.get("height_m", 0.4),
            materials=mats)
        cbu.mark_static_collider(c_in)
        cbu.add_custom_property(c_in, "unity_tag", "Conveyor")
        cbu.add_custom_property(c_in, "connects_from", conv_in.get("from", "S01"))
        top_level.append(c_in)

    if conv_out:
        c_out = cbu.create_simple_conveyor(
            "CONVEYOR_Assembly_Output", start=conv_out["start"], end=conv_out["end"],
            width=conv_out.get("width_m", 0.6), height=conv_out.get("height_m", 0.4),
            materials=mats)
        cbu.mark_static_collider(c_out)
        cbu.add_custom_property(c_out, "unity_tag", "Conveyor")
        cbu.add_custom_property(c_out, "connects_to", conv_out.get("to", "S03"))
        top_level.append(c_out)

    # --- Info panel facing the avatar walkway (+Y) -------------------------
    ip_pos = info.get("position", [px, py + 2.6, 1.6])
    ip_text = info.get("text", "Assisted Assembly Station")
    info_panel = cbu.create_info_panel(
        "INFO_Assembly_Panel", title="Assisted Assembly", body=ip_text,
        location=tuple(ip_pos), rotation=(0, 0, math.radians(180)),
        materials=mats)
    top_level.append(info_panel)

    # --- Info trigger zone -------------------------------------------------
    trigger = cbu.create_trigger_zone(
        "TRIGGER_Info_Assembly",
        location=(ip_pos[0], ip_pos[1] + 0.7, 1.1),
        scale=(2.4, 1.6, 2.2))
    cbu.add_custom_property(trigger, "station_id", STATION_ID)
    top_level.append(trigger)

    for obj in top_level:
        _parent_keep(obj, root)

    return root, coll


# ---------------------------------------------------------------------------
# Review scene
# ---------------------------------------------------------------------------

def setup_review_scene(station_center):
    mats = cbu.create_default_materials()
    cx, cy = station_center
    floor = cbu.create_cube(
        "PHYS_Assembly_FloorPatch",
        location=(cx, cy + 1.0, -0.05), scale=(7.0, 8.0, 0.1),
        material=mats["white_panel"])
    cbu.add_custom_property(floor, "unity_tag", "Floor")
    cbu.mark_static_collider(floor)

    cbu.setup_lighting()

    cam = cbu.setup_camera(location=(cx + 2.6, cy + 5.2, 3.2), focal_length=35.0)
    _aim_camera_at(cam, (cx, cy - 0.2, 1.1))
    return cam


def render_screenshot(path):
    try:
        scene = bpy.context.scene
        try:
            scene.render.engine = "BLENDER_EEVEE_NEXT"
        except (TypeError, AttributeError):
            pass
        scene.render.resolution_x = 1280
        scene.render.resolution_y = 720
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = "PNG"
        cbu.ensure_dir(path)
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        return os.path.exists(path)
    except Exception as exc:  # noqa: BLE001
        print("[assembly] screenshot skipped:", exc)
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cbu.clear_scene()
    cbu.set_units_to_meters()

    root, _coll = build_assembly_station()
    station_center = (root.location.x, root.location.y)
    setup_review_scene(station_center)

    blend_path = os.path.join(_B_ROOT, "exports", "blend", "02_assembly_station.blend")
    glb_path = os.path.join(_B_ROOT, "exports", "glb", "02_assembly_station.glb")
    png_path = os.path.join(_B_ROOT, "exports", "screenshots", "02_assembly_station.png")

    cbu.save_blend(blend_path)
    cbu.export_glb(glb_path)
    shot_ok = render_screenshot(png_path)

    print("[assembly] saved blend :", blend_path)
    print("[assembly] exported glb:", glb_path)
    print("[assembly] screenshot  :", png_path if shot_ok else "(not created)")


if __name__ == "__main__":
    main()
