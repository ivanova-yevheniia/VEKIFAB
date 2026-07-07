"""
component_registry.py — Generic component type -> builder function registry.

Maps a generic component/primitive type (cube, cylinder, roller, frame, panel,
label, light, cabinet, beam, profile, conveyor, shelf, box, ...) to a builder
callable. Nothing here is station-specific.

Each builder has the signature:

    build(ctx, name, node, center, rotation_deg, material_key, parent) -> obj

`center` (world position), `name`, `material_key` and instance rotation are
resolved by the scene builder; the component builder only turns one node into
one Blender object of the requested type. New types can be added at runtime via
``register(...)`` without modifying the scene builder.
"""

import math

import geometry_builder as gb

REGISTRY = {}


def register(*types):
    """Decorator: register a builder under one or more generic type names."""
    def _wrap(fn):
        for t in types:
            REGISTRY[t] = fn
        return fn
    return _wrap


def get_builder(component_type):
    return REGISTRY.get(component_type)


def known_types():
    return set(REGISTRY.keys())


# ---------------------------------------------------------------------------
# Box-like builders (cube / structural members / flat panels)
# ---------------------------------------------------------------------------

@register("box", "cube", "beam", "profile", "frame", "panel", "shelf", "cabinet",
          "conveyor")
def build_box(ctx, name, node, center, rotation_deg, material_key, parent):
    # Box sized either by explicit dimensions, a cube size, or a start/end span.
    if "start_world_m" in node and "end_world_m" in node:
        a, b = node["start_world_m"], node["end_world_m"]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = max(math.hypot(dx, dy), 1e-4)
        width = float(node.get("width_m", 0.5))
        thick = float(node.get("belt_thickness_m", node.get("height_m", 0.1)))
        size = (length, width, thick)
        rotation_deg = [0.0, 0.0, math.degrees(math.atan2(dy, dx))]
    elif "dimensions_m" in node:
        size = node["dimensions_m"]
    elif "cube_size_m" in node:
        s = float(node["cube_size_m"])
        size = (s, s, s)
    else:
        size = (0.1, 0.1, 0.1)
        ctx.warnings.append("box '%s' has no size; defaulting" % name)

    obj = gb.create_box(ctx, name, center, size, material_key)
    if rotation_deg:
        gb.set_rotation(obj, rotation_deg)
    if "bevel_m" in node:
        gb.add_bevel(obj, node["bevel_m"], ctx.bevel_segments(node.get("bevel_segments")))
    gb.apply_flags(obj, node)
    gb.parent_keep(obj, parent)
    return obj


# ---------------------------------------------------------------------------
# Cylinder-like builders (rollers, posts, buttons, poles)
# ---------------------------------------------------------------------------

@register("cylinder", "roller", "post", "pole")
def build_cylinder(ctx, name, node, center, rotation_deg, material_key, parent):
    radius = float(node.get("radius_m", 0.05))
    depth = float(node.get("depth_m", node.get("segment_height_m", 0.1)))
    obj = gb.create_cylinder(ctx, name, center, radius, depth, material_key,
                            vertices=node.get("vertices"), axis=node.get("axis", "Z"))
    if rotation_deg:
        # Compose over any axis rotation already applied.
        base = obj.rotation_euler.copy()
        extra = [math.radians(float(a)) for a in rotation_deg]
        obj.rotation_euler = (base[0] + extra[0], base[1] + extra[1], base[2] + extra[2])
    if "bevel_m" in node:
        gb.add_bevel(obj, node["bevel_m"], ctx.bevel_segments(node.get("bevel_segments")))
    gb.apply_flags(obj, node)
    gb.parent_keep(obj, parent)
    return obj


# ---------------------------------------------------------------------------
# Empty (structural roots / anchors)
# ---------------------------------------------------------------------------

@register("empty")
def build_empty(ctx, name, node, center, rotation_deg, material_key, parent):
    obj = gb.create_empty(ctx, name, center, etype=node.get("empty_type", "PLAIN_AXES"))
    if rotation_deg:
        gb.set_rotation(obj, rotation_deg)
    gb.apply_flags(obj, node)
    gb.parent_keep(obj, parent)
    return obj


# ---------------------------------------------------------------------------
# Text / label
# ---------------------------------------------------------------------------

@register("text_mesh", "quad_or_text_mesh", "label", "text")
def build_text(ctx, name, node, center, rotation_deg, material_key, parent):
    text = node.get("text", "")
    size = float(node.get("size_m", 0.1))
    obj = gb.create_text(ctx, name, text, center, rotation_deg or (0, 0, 0), size,
                        material_key, wrap_chars=node.get("wrap_chars"))
    gb.apply_flags(obj, node)
    gb.parent_keep(obj, parent)
    return obj


# ---------------------------------------------------------------------------
# Light
# ---------------------------------------------------------------------------

@register("light")
def build_light(ctx, name, node, center, rotation_deg, material_key, parent):
    obj = gb.create_light(ctx, name, center, ltype=node.get("type", "AREA"),
                         energy=node.get("energy_w", 100.0),
                         size=node.get("size_m", 0.5))
    if rotation_deg:
        gb.set_rotation(obj, rotation_deg)
    gb.parent_keep(obj, parent)
    return obj
