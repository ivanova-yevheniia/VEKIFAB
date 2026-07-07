"""
geometry_builder.py — Generic Blender geometry primitives for WP B.

Station-agnostic. This module knows NOTHING about loading, assembly, robots,
etc. It only creates generic Blender objects (box, cylinder, empty, text,
light) from plain numeric descriptions and applies generic operations
(bevel, smooth shading, rotation, material, Unity flags, parenting).

All geometry is created from values supplied by the caller — this module holds
no station dimensions of its own.
"""

import math

try:
    import bpy
    from mathutils import Vector, Matrix  # noqa: F401
    _HAS_BPY = True
except ImportError:
    bpy = None
    Vector = None
    Matrix = None
    _HAS_BPY = False


class BuildContext:
    """Carries shared state through a build (materials, object table, defaults)."""

    def __init__(self, mat_engine, station_origin, rules=None, collection=None):
        self.mat = mat_engine
        self.origin = station_origin
        self.rules = rules or {}
        self.collection = collection
        self.objects = {}          # name -> bpy object
        self.warnings = []         # human-readable strings

    # -- defaults pulled from industrial_rules (never hardcoded here) --------
    def cyl_vertices(self, requested=None):
        if requested:
            return int(requested)
        perf = self.rules.get("performance_rules", {})
        tiers = perf.get("cylinder_vertices", {})
        return int(tiers.get("medium", 16))

    def bevel_segments(self, requested=None):
        if requested is not None:
            return int(requested)
        perf = self.rules.get("performance_rules", {})
        return int(perf.get("bevel_segments_max", 2))

    def register(self, obj):
        if obj is None:
            return obj
        if obj.name in self.objects and self.objects[obj.name] is not obj:
            self.warnings.append("duplicate object name: %s" % obj.name)
        self.objects[obj.name] = obj
        return obj


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _v(value):
    return Vector((float(value[0]), float(value[1]), float(value[2])))


def _radians3(deg):
    if not deg:
        return (0.0, 0.0, 0.0)
    return tuple(math.radians(float(a)) for a in deg)


def apply_material(ctx, obj, material_key):
    """Append a material (by library key) to an object; no-op if key is falsy."""
    if not material_key or obj is None or not hasattr(obj.data, "materials"):
        return
    mat = ctx.mat.get(material_key)
    if mat is not None:
        obj.data.materials.append(mat)


def add_bevel(obj, width, segments=2):
    mod = obj.modifiers.new(name="Bevel", type="BEVEL")
    mod.width = float(width)
    mod.segments = int(segments)
    mod.limit_method = "ANGLE"
    return mod


def shade_smooth(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = True


def set_rotation(obj, rotation_deg):
    obj.rotation_euler = _radians3(rotation_deg)


def parent_keep(child, parent):
    """Parent while preserving world transform (avoids double-translation)."""
    if parent is None or child is None:
        return
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()


def apply_flags(obj, node):
    """Write generic Unity handoff flags as custom properties (glTF extras)."""
    if obj is None:
        return
    collider = node.get("collider")
    if collider:
        obj["collider"] = True
        obj["collider_type"] = collider if isinstance(collider, str) else "static"
        obj["rigidbody"] = False
    rb = node.get("rigidbody")
    if isinstance(rb, dict) and rb.get("enabled"):
        obj["rigidbody"] = True
        obj["mass"] = float(rb.get("mass_kg", 1.0))
        obj["kinematic"] = bool(rb.get("kinematic", False))
    if node.get("is_trigger"):
        obj["collider"] = True
        obj["is_trigger"] = True
        obj["unity_tag"] = "Trigger"
    if node.get("unity_tag"):
        obj["unity_tag"] = node["unity_tag"]
    if node.get("display") == "wire":
        obj.display_type = "WIRE"
    if node.get("hide_render"):
        obj.hide_render = True


# ---------------------------------------------------------------------------
# Primitive creators
# ---------------------------------------------------------------------------

def create_box(ctx, name, center, size, material_key=None):
    """A box of full dimensions `size` centred at `center` (metres)."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=tuple(center))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (float(size[0]), float(size[1]), float(size[2]))
    apply_material(ctx, obj, material_key)
    return ctx.register(obj)


def create_cylinder(ctx, name, center, radius, depth, material_key=None,
                    vertices=None, axis="Z"):
    """A cylinder centred at `center`. `axis` orients the depth direction."""
    verts = ctx.cyl_vertices(vertices)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=float(radius), depth=float(depth), vertices=verts,
        location=tuple(center))
    obj = bpy.context.active_object
    obj.name = name
    if axis == "Y":
        obj.rotation_euler = (math.radians(90), 0.0, 0.0)
    elif axis == "X":
        obj.rotation_euler = (0.0, math.radians(90), 0.0)
    shade_smooth(obj)
    apply_material(ctx, obj, material_key)
    return ctx.register(obj)


def create_empty(ctx, name, location, etype="PLAIN_AXES"):
    bpy.ops.object.empty_add(type=etype, location=tuple(location))
    obj = bpy.context.active_object
    obj.name = name
    return ctx.register(obj)


def _wrap_text(text, max_chars):
    if not max_chars:
        return text
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = w if not cur else cur + " " + w
        if len(cand) > max_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def create_text(ctx, name, text, center, rotation_deg, size, material_key=None,
               wrap_chars=None):
    """A text label converted to mesh (font objects do not export to glTF)."""
    bpy.ops.object.text_add(location=tuple(center), rotation=_radians3(rotation_deg))
    obj = bpy.context.active_object
    obj.name = name
    obj.data.body = _wrap_text(text, wrap_chars)
    obj.data.size = float(size)
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    apply_material(ctx, obj, material_key)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target="MESH")
    obj = bpy.context.active_object
    obj.name = name
    return ctx.register(obj)


def create_light(ctx, name, center, ltype="AREA", energy=100.0, size=0.5):
    data = bpy.data.lights.new(name, type=ltype)
    data.energy = float(energy)
    if hasattr(data, "size"):
        try:
            data.size = float(size)
        except (AttributeError, TypeError):
            pass
    obj = bpy.data.objects.new(name, data)
    obj.location = tuple(center)
    (ctx.collection or bpy.context.collection).objects.link(obj)
    return ctx.register(obj)
