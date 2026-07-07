"""
common_blender_utils.py — Shared Blender helpers for the VEKIFAB WP B generators.

This module centralises everything the individual station generators need so the
exported scene stays clean, lightweight and consistent for Unity:

  * Scene setup (units, camera, lighting, factory floor).
  * A reusable default material palette.
  * Lightweight geometry helpers (cubes, cylinders, bevel, smooth, text).
  * Simple industrial components (control panel, e-stop, info panel, conveyor).
  * Unity handoff helpers (custom properties, collider / rigidbody / trigger tags).
  * IO helpers (load JSON, ensure dir, save .blend, export .glb).

Object naming follows the WP B conventions (see docs/unity_import_notes.md):
    STATION_*, CONVEYOR_*, PHYS_*, COLLIDER_*, TRIGGER_*, INFO_*

Only the built-in Blender Python API (`bpy`) is used. `bpy` is only available
inside Blender, so it is imported at module top but the module still imports
cleanly enough to be introspected; the functions themselves require Blender.

Nothing runs on import except the small smoke test under
`if __name__ == "__main__"`.
"""

import os
import json
import math

try:
    import bpy
    import mathutils  # noqa: F401  (available inside Blender; used for vectors)
    _HAS_BPY = True
except ImportError:  # Allows the file to be imported/inspected outside Blender.
    bpy = None
    _HAS_BPY = False


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

def _b_blender_root() -> str:
    """Return the absolute path of the B_Blender/ directory.

    Works both when run as a file (``__file__`` available) and from Blender's
    text editor (falls back to the current working directory).
    """
    try:
        here = os.path.dirname(os.path.abspath(__file__))  # .../B_Blender/generators
        return os.path.dirname(here)                        # .../B_Blender
    except NameError:
        return os.getcwd()


# ===========================================================================
# 1. Scene setup
# ===========================================================================

def clear_scene():
    """Remove all objects and purge orphan data so we start from a clean scene."""
    if not _HAS_BPY:
        raise RuntimeError("clear_scene() requires Blender (bpy).")
    # Delete all objects.
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    # Purge orphaned meshes, materials, cameras, lights, curves.
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras,
                 bpy.data.lights, bpy.data.curves):
        for block in list(coll):
            if block.users == 0:
                coll.remove(block)


def set_units_to_meters():
    """Configure the scene unit system to metric metres (matches Unity 1 = 1 m)."""
    if not _HAS_BPY:
        raise RuntimeError("set_units_to_meters() requires Blender (bpy).")
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    scene.unit_settings.scale_length = 1.0


def setup_camera(location=(20.0, -18.0, 14.0),
                 rotation=(math.radians(60), 0.0, math.radians(40)),
                 focal_length=35.0):
    """Create a scene camera looking over the line.

    Args:
        location: World-space camera position (metres).
        rotation: Euler rotation in radians.
        focal_length: Lens focal length in millimetres.

    Returns:
        The created camera object.
    """
    if not _HAS_BPY:
        raise RuntimeError("setup_camera() requires Blender (bpy).")
    cam_data = bpy.data.cameras.new("CAM_Main")
    cam_data.lens = focal_length
    cam_obj = bpy.data.objects.new("CAM_Main", cam_data)
    cam_obj.location = location
    cam_obj.rotation_euler = rotation
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    return cam_obj


def setup_lighting():
    """Add basic, even lighting: one sun plus a soft world ambient.

    Returns:
        The created sun light object.
    """
    if not _HAS_BPY:
        raise RuntimeError("setup_lighting() requires Blender (bpy).")
    # Key sun light.
    sun_data = bpy.data.lights.new("LIGHT_Sun", type="SUN")
    sun_data.energy = 3.0
    sun_obj = bpy.data.objects.new("LIGHT_Sun", sun_data)
    sun_obj.location = (10.0, -10.0, 20.0)
    sun_obj.rotation_euler = (math.radians(45), math.radians(15), math.radians(30))
    bpy.context.collection.objects.link(sun_obj)

    # Soft ambient via the world background.
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg is not None:
        bg.inputs["Color"].default_value = (0.6, 0.62, 0.65, 1.0)
        bg.inputs["Strength"].default_value = 0.4
    return sun_obj


def create_factory_floor(length, width, name="PHYS_Floor", material=None):
    """Create the factory floor slab, origin at one corner (0,0).

    Args:
        length: Floor size along X (metres).
        width: Floor size along Y (metres).
        name: Object name (Unity-friendly).
        material: Optional material to assign.

    Returns:
        The floor object (marked as a static collider, tagged 'Floor').
    """
    if not _HAS_BPY:
        raise RuntimeError("create_factory_floor() requires Blender (bpy).")
    thickness = 0.1
    obj = create_cube(
        name,
        location=(length / 2.0, width / 2.0, -thickness / 2.0),
        scale=(length, width, thickness),
        material=material,
    )
    add_custom_property(obj, "unity_tag", "Floor")
    mark_static_collider(obj)
    return obj


# ===========================================================================
# 2. Materials
# ===========================================================================

def _principled(mat):
    """Return the Principled BSDF node of a node-based material (or None)."""
    node = mat.node_tree.nodes.get("Principled BSDF")
    if node is None:
        for n in mat.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED":
                return n
    return node


def create_material(name, color, metallic=0.0, roughness=0.5, alpha=1.0):
    """Create (or reuse) a Principled BSDF material.

    Args:
        name: Material name (Unity-friendly, e.g. 'MAT_MetalDark').
        color: RGBA tuple in 0..1.
        metallic: 0..1 metallic factor.
        roughness: 0..1 roughness factor.
        alpha: 0..1 opacity (values < 1 switch the material to alpha blend).

    Returns:
        The material data-block.
    """
    if not _HAS_BPY:
        raise RuntimeError("create_material() requires Blender (bpy).")
    if name in bpy.data.materials:
        return bpy.data.materials[name]

    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = _principled(mat)
    if bsdf is not None:
        # Ensure a 4-component colour.
        if len(color) == 3:
            color = (color[0], color[1], color[2], alpha)
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        # Enable transparency (property name varies across Blender versions).
        try:
            mat.blend_method = "BLEND"
        except (AttributeError, TypeError):
            pass
    # Viewport display colour for a readable solid-shading preview.
    mat.diffuse_color = color if len(color) == 4 else (color[0], color[1], color[2], alpha)
    return mat


def _set_emission(mat, color, strength=2.0):
    """Add an emissive glow to a material (used for indicator lights/screens)."""
    bsdf = _principled(mat)
    if bsdf is None:
        return
    rgba = color if len(color) == 4 else (color[0], color[1], color[2], 1.0)
    # Emission input renamed to 'Emission Color' in Blender 4.x.
    for key in ("Emission Color", "Emission"):
        if key in bsdf.inputs:
            bsdf.inputs[key].default_value = rgba
            break
    if "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Strength"].default_value = strength


def create_default_materials():
    """Create the WP B default material palette.

    Returns:
        dict mapping short keys to material data-blocks:
        metal_dark, metal_light, white_panel, blue_accent, safety_yellow,
        warning_black, rubber_black, glass_clear, screen_dark, red_emergency,
        green_light.
    """
    if not _HAS_BPY:
        raise RuntimeError("create_default_materials() requires Blender (bpy).")

    mats = {
        "metal_dark":    create_material("MAT_MetalDark",   (0.15, 0.15, 0.17, 1.0), metallic=0.9, roughness=0.40),
        "metal_light":   create_material("MAT_MetalLight",  (0.70, 0.72, 0.75, 1.0), metallic=0.9, roughness=0.30),
        "white_panel":   create_material("MAT_WhitePanel",  (0.90, 0.90, 0.92, 1.0), metallic=0.0, roughness=0.50),
        "blue_accent":   create_material("MAT_BlueAccent",  (0.10, 0.35, 0.75, 1.0), metallic=0.1, roughness=0.40),
        "safety_yellow": create_material("MAT_SafetyYellow",(0.95, 0.80, 0.05, 1.0), metallic=0.0, roughness=0.60),
        "warning_black": create_material("MAT_WarningBlack",(0.03, 0.03, 0.03, 1.0), metallic=0.0, roughness=0.70),
        "rubber_black":  create_material("MAT_RubberBlack", (0.05, 0.05, 0.05, 1.0), metallic=0.0, roughness=0.90),
        "glass_clear":   create_material("MAT_GlassClear",  (0.80, 0.85, 0.90, 0.2), metallic=0.0, roughness=0.05, alpha=0.2),
        "screen_dark":   create_material("MAT_ScreenDark",  (0.02, 0.02, 0.03, 1.0), metallic=0.0, roughness=0.20),
        "red_emergency": create_material("MAT_RedEmergency",(0.80, 0.05, 0.05, 1.0), metallic=0.0, roughness=0.40),
        "green_light":   create_material("MAT_GreenLight",  (0.05, 0.80, 0.20, 1.0), metallic=0.0, roughness=0.40),
    }
    # Give the indicator lights / screen a subtle emissive glow.
    _set_emission(mats["screen_dark"],   (0.10, 0.35, 0.55, 1.0), strength=1.0)
    _set_emission(mats["red_emergency"], (0.80, 0.05, 0.05, 1.0), strength=3.0)
    _set_emission(mats["green_light"],   (0.05, 0.80, 0.20, 1.0), strength=3.0)
    return mats


# ===========================================================================
# 3. Geometry helpers
# ===========================================================================

def _assign_material(obj, material):
    """Append a material to an object's mesh (no-op if material is None)."""
    if material is not None:
        obj.data.materials.append(material)


def _parent_keep(child, parent):
    """Parent ``child`` to ``parent`` while preserving its world transform.

    Setting ``child.parent`` alone leaves ``matrix_parent_inverse`` as identity,
    which double-translates the child by the parent's location. Capturing the
    parent's inverse world matrix here keeps the child where it was placed.
    """
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()


def create_cube(name, location, scale, material=None):
    """Create a box.

    Args:
        name: Object name.
        location: World-space centre (metres).
        scale: Full size (x, y, z) in metres — a size-1 cube scaled to these.
        material: Optional material.

    Returns:
        The mesh object.
    """
    if not _HAS_BPY:
        raise RuntimeError("create_cube() requires Blender (bpy).")
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (scale[0], scale[1], scale[2])
    _assign_material(obj, material)
    return obj


def create_cylinder(name, location, radius, depth, material=None, vertices=32):
    """Create a cylinder.

    Args:
        name: Object name.
        location: World-space centre (metres).
        radius: Radius (metres).
        depth: Height along Z (metres).
        material: Optional material.
        vertices: Radial segment count (kept low for lightweight geometry).

    Returns:
        The mesh object.
    """
    if not _HAS_BPY:
        raise RuntimeError("create_cylinder() requires Blender (bpy).")
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, vertices=vertices, location=location)
    obj = bpy.context.active_object
    obj.name = name
    _assign_material(obj, material)
    return obj


def add_bevel_modifier(obj, amount=0.03, segments=2):
    """Add a small bevel modifier to soften hard edges.

    Returns:
        The bevel modifier.
    """
    if not _HAS_BPY:
        raise RuntimeError("add_bevel_modifier() requires Blender (bpy).")
    mod = obj.modifiers.new(name="Bevel", type="BEVEL")
    mod.width = amount
    mod.segments = segments
    mod.limit_method = "ANGLE"
    return mod


def shade_smooth(obj):
    """Set smooth shading on all faces of a mesh object (context-independent)."""
    if not _HAS_BPY:
        raise RuntimeError("shade_smooth() requires Blender (bpy).")
    mesh = obj.data
    for poly in mesh.polygons:
        poly.use_smooth = True


def create_text_label(name, text, location, rotation=(0, 0, 0), size=0.25,
                      material=None, convert_to_mesh=True):
    """Create a text label, optionally converted to mesh for reliable glTF export.

    Args:
        name: Object name.
        text: The string to display.
        location: World-space position (metres).
        rotation: Euler rotation in radians.
        size: Font size (metres).
        material: Optional material.
        convert_to_mesh: If True, convert the font object to a mesh so it exports
            cleanly to .glb (Blender text objects do not export to glTF).

    Returns:
        The label object (font or mesh).
    """
    if not _HAS_BPY:
        raise RuntimeError("create_text_label() requires Blender (bpy).")
    bpy.ops.object.text_add(location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.body = text
    obj.data.size = size
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    _assign_material(obj, material)
    if convert_to_mesh:
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target="MESH")
        obj = bpy.context.active_object
        obj.name = name
    return obj


# ===========================================================================
# 4. Industrial components
# ===========================================================================

def create_control_panel(name, location, rotation=(0, 0, 0), materials=None):
    """Create a simple control panel: a body with a dark screen face.

    Args:
        name: Object name (e.g. 'PHYS_Station_Panel').
        location: World-space base position (metres).
        rotation: Euler rotation in radians (applied to the parent).
        materials: Optional default-materials dict (from create_default_materials).

    Returns:
        The panel body object (with the screen parented to it).
    """
    if not _HAS_BPY:
        raise RuntimeError("create_control_panel() requires Blender (bpy).")
    body_mat = materials.get("metal_light") if materials else None
    screen_mat = materials.get("screen_dark") if materials else None

    body = create_cube(name, location=location, scale=(0.5, 0.15, 0.7),
                       material=body_mat)
    add_bevel_modifier(body)
    # Screen slightly in front of the body (+Y face).
    screen = create_cube(name + "_Screen",
                        location=(location[0], location[1] - 0.09, location[2] + 0.1),
                        scale=(0.36, 0.02, 0.28), material=screen_mat)
    _parent_keep(screen, body)
    body.rotation_euler = rotation
    return body


def create_emergency_stop(name, location, materials=None):
    """Create a red emergency-stop button on a yellow backing plate.

    Returns:
        The button object (mushroom cap), with the plate parented to it.
    """
    if not _HAS_BPY:
        raise RuntimeError("create_emergency_stop() requires Blender (bpy).")
    yellow = materials.get("safety_yellow") if materials else None
    red = materials.get("red_emergency") if materials else None

    plate = create_cube(name + "_Plate", location=location,
                       scale=(0.16, 0.05, 0.16), material=yellow)
    button = create_cylinder(name,
                           location=(location[0], location[1] - 0.05, location[2]),
                           radius=0.04, depth=0.05, material=red, vertices=16)
    button.rotation_euler = (math.radians(90), 0, 0)  # face outward (+Y).
    shade_smooth(button)
    _parent_keep(plate, button)
    add_custom_property(button, "unity_tag", "EmergencyStop")
    return button


def _wrap_text(text, max_chars=30):
    """Greedy word-wrap a string into lines of at most ``max_chars`` characters.

    Keeps info-panel body text inside the board instead of overflowing it.
    """
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = word if not current else current + " " + word
        if len(candidate) > max_chars and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return "\n".join(lines)


def create_info_panel(name, title, body, location, rotation=(0, 0, 0),
                      materials=None):
    """Create an INFO_ panel: a white board with a title and body text.

    Args:
        name: Object name (should start with 'INFO_').
        title: Panel heading text.
        body: Panel body text.
        location: World-space centre of the board (metres).
        rotation: Euler rotation in radians (board faces +Y at 0).
        materials: Optional default-materials dict.

    Returns:
        The board object (title and body labels parented to it).
    """
    if not _HAS_BPY:
        raise RuntimeError("create_info_panel() requires Blender (bpy).")
    board_mat = materials.get("white_panel") if materials else None
    text_mat = materials.get("warning_black") if materials else None

    board = create_cube(name, location=location, scale=(1.2, 0.05, 0.7),
                      material=board_mat)
    add_bevel_modifier(board, amount=0.02)

    # Text sits just in front of the board (-Y side, i.e. facing the walkway).
    ty = location[1] - 0.04
    title_obj = create_text_label(
        name + "_Title", title,
        location=(location[0], ty, location[2] + 0.22),
        rotation=(math.radians(90), 0, 0), size=0.13, material=text_mat)
    body_obj = create_text_label(
        name + "_Body", _wrap_text(body, max_chars=28),
        location=(location[0], ty, location[2] - 0.08),
        rotation=(math.radians(90), 0, 0), size=0.06, material=text_mat)
    _parent_keep(title_obj, board)
    _parent_keep(body_obj, board)

    board.rotation_euler = rotation
    add_custom_property(board, "unity_tag", "InfoPanel")
    add_custom_property(board, "info_title", title)
    add_custom_property(board, "info_body", body)
    return board


def create_warning_floor_marking(name, location, scale, materials=None):
    """Create a thin yellow floor marking (e.g. a keep-out / walkway stripe).

    Args:
        name: Object name.
        location: World-space centre (metres); Z is set just above the floor.
        scale: Full (x, y) size in metres (z is forced thin).
        materials: Optional default-materials dict.

    Returns:
        The marking object.
    """
    if not _HAS_BPY:
        raise RuntimeError("create_warning_floor_marking() requires Blender (bpy).")
    yellow = materials.get("safety_yellow") if materials else None
    obj = create_cube(name,
                     location=(location[0], location[1], 0.01),
                     scale=(scale[0], scale[1], 0.02), material=yellow)
    add_custom_property(obj, "unity_tag", "FloorMarking")
    return obj


def create_simple_conveyor(name, start, end, width=0.8, height=0.4,
                           materials=None):
    """Create a simple straight conveyor belt between two points.

    The belt is a single box oriented along the start→end direction (assumed to
    lie in the XY plane). Kept deliberately lightweight.

    Args:
        name: Object name (should start with 'CONVEYOR_').
        start: (x, y, z) start point.
        end: (x, y, z) end point.
        width: Belt width (metres).
        height: Belt top height above the floor (metres).
        materials: Optional default-materials dict.

    Returns:
        The conveyor belt object (tagged 'Conveyor', kinematic rigid body).
    """
    if not _HAS_BPY:
        raise RuntimeError("create_simple_conveyor() requires Blender (bpy).")
    belt_mat = materials.get("rubber_black") if materials else None
    frame_mat = materials.get("metal_dark") if materials else None

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = max(math.hypot(dx, dy), 0.01)
    angle = math.atan2(dy, dx)
    cx = (start[0] + end[0]) / 2.0
    cy = (start[1] + end[1]) / 2.0
    belt_thickness = 0.06

    belt = create_cube(name,
                     location=(cx, cy, height),
                     scale=(length, width, belt_thickness), material=belt_mat)
    belt.rotation_euler = (0, 0, angle)

    # Simple support frame under the belt.
    frame = create_cube(name + "_Frame",
                      location=(cx, cy, height / 2.0),
                      scale=(length, width * 0.9, height - belt_thickness),
                      material=frame_mat)
    frame.rotation_euler = (0, 0, angle)
    _parent_keep(frame, belt)

    add_custom_property(belt, "unity_tag", "Conveyor")
    add_custom_property(belt, "belt_speed_mps", 0.15)
    mark_rigidbody(belt, mass=0.0, kinematic=True)
    mark_static_collider(frame)
    return belt


# ===========================================================================
# 5. Unity helpers
# ===========================================================================

def add_custom_property(obj, key, value):
    """Set a custom property (exported to glTF 'extras', read by Unity import)."""
    if not _HAS_BPY:
        raise RuntimeError("add_custom_property() requires Blender (bpy).")
    obj[key] = value
    return obj


def mark_static_collider(obj):
    """Tag an object as a static collider for the Unity importer.

    Tags via custom properties (naming convention COLLIDER_* is applied by the
    caller when the object is a dedicated collision proxy).
    """
    if not _HAS_BPY:
        raise RuntimeError("mark_static_collider() requires Blender (bpy).")
    add_custom_property(obj, "collider", True)
    add_custom_property(obj, "collider_type", "static")
    add_custom_property(obj, "rigidbody", False)
    return obj


def mark_rigidbody(obj, mass=1.0, kinematic=False):
    """Tag an object as a Unity rigid body (mass + kinematic flag).

    Physics is expressed as glTF extras for Unity; no Blender rigid-body world
    is created, to keep the export lightweight.
    """
    if not _HAS_BPY:
        raise RuntimeError("mark_rigidbody() requires Blender (bpy).")
    add_custom_property(obj, "rigidbody", True)
    add_custom_property(obj, "mass", float(mass))
    add_custom_property(obj, "kinematic", bool(kinematic))
    return obj


def mark_trigger(obj):
    """Tag an object as a non-blocking trigger volume for Unity."""
    if not _HAS_BPY:
        raise RuntimeError("mark_trigger() requires Blender (bpy).")
    add_custom_property(obj, "collider", True)
    add_custom_property(obj, "is_trigger", True)
    add_custom_property(obj, "unity_tag", "Trigger")
    return obj


def create_trigger_zone(name, location, scale, materials=None):
    """Create an invisible trigger volume (wireframe box) for inspection events.

    Args:
        name: Object name (should start with 'TRIGGER_').
        location: World-space centre (metres).
        scale: Full (x, y, z) size in metres.
        materials: Unused (kept for signature symmetry); triggers render as wire.

    Returns:
        The trigger object (display type WIRE, tagged as a trigger).
    """
    if not _HAS_BPY:
        raise RuntimeError("create_trigger_zone() requires Blender (bpy).")
    obj = create_cube(name, location=location, scale=scale, material=None)
    obj.display_type = "WIRE"
    obj.hide_render = True  # invisible in renders; volume still exported for Unity.
    mark_trigger(obj)
    return obj


# ===========================================================================
# 6. IO helpers
# ===========================================================================

def load_json(path):
    """Load and return a JSON file as a Python object."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def ensure_dir(path):
    """Ensure the directory for ``path`` exists.

    If ``path`` looks like a file (has an extension), its parent directory is
    created; otherwise ``path`` itself is created.
    """
    directory = path
    if os.path.splitext(path)[1]:  # has a file extension
        directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    return directory


def save_blend(path):
    """Save the current scene as a .blend file (creating parent dirs)."""
    if not _HAS_BPY:
        raise RuntimeError("save_blend() requires Blender (bpy).")
    ensure_dir(path)
    bpy.ops.wm.save_as_mainfile(filepath=path)
    return path


def export_glb(path):
    """Export the whole scene to a binary glTF (.glb) for Unity (Y-up)."""
    if not _HAS_BPY:
        raise RuntimeError("export_glb() requires Blender (bpy).")
    ensure_dir(path)
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format="GLB",
        export_yup=True,                 # Y-up for Unity.
        export_apply=True,               # apply modifiers.
        export_extras=True,              # include custom properties as 'extras'.
        use_selection=False,
    )
    return path


# ===========================================================================
# Smoke test
# ===========================================================================

def _smoke_test():
    """Build a minimal scene (floor + cube + light + camera) and export it.

    Writes:
        B_Blender/exports/blend/utils_smoke_test.blend
        B_Blender/exports/glb/utils_smoke_test.glb
    """
    root = _b_blender_root()
    blend_path = os.path.join(root, "exports", "blend", "utils_smoke_test.blend")
    glb_path = os.path.join(root, "exports", "glb", "utils_smoke_test.glb")

    clear_scene()
    set_units_to_meters()
    mats = create_default_materials()

    create_factory_floor(25.0, 18.0, material=mats["white_panel"])
    cube = create_cube("PHYS_TestCube", location=(3.0, 3.0, 0.5),
                       scale=(1.0, 1.0, 1.0), material=mats["blue_accent"])
    add_bevel_modifier(cube)
    shade_smooth(cube)
    mark_static_collider(cube)

    setup_lighting()
    setup_camera()

    save_blend(blend_path)
    export_glb(glb_path)

    print("[smoke test] saved blend:", blend_path)
    print("[smoke test] exported glb:", glb_path)
    return blend_path, glb_path


if __name__ == "__main__":
    if _HAS_BPY:
        _smoke_test()
    else:
        print("common_blender_utils.py: bpy not available — run this inside Blender.")
