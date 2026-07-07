"""
scene_builder.py — Generic scene assembly from a parameter specification.

Walks a station parameter file's `components` tree and builds every generic
component. It knows only a small, generic "node grammar" (below) — never any
station concept. Naming, positions and materials all come from the JSON.

Node grammar
------------
A *node* is any dict with a ``primitive`` key. It produces one object, or N
objects when it carries ``count`` plus a layout:
  * ``offsets_m``        : explicit list of [dx,dy,dz] (relative to origin)
  * ``start_offset_m`` + ``step_m`` : linear array
  * ``stack``            : layered grid (grid_offsets_m, layers, heights)
  * inherited            : reuse a sibling array's offsets of matching count
Positions resolve via ``world_position_m`` (absolute), ``offset_m`` (origin +
offset), ``offset_from_parent_m`` (parent-local), or a ``start_world_m`` /
``end_world_m`` midpoint.

A *container* is a dict without ``primitive`` whose child dicts are nodes or
containers. The container's ``naming`` is applied to its primary child; other
children parent to that primary. A dict with a light ``type`` (AREA/POINT/...)
is built as a light.
"""

import geometry_builder as gb
import component_registry as registry
from material_engine import MaterialEngine

try:
    import bpy
    from mathutils import Vector
    _HAS_BPY = True
except ImportError:
    bpy = None
    Vector = None
    _HAS_BPY = False

_LIGHT_TYPES = {"AREA", "POINT", "SUN", "SPOT"}
_PRIMARY_KEYS = ("worktop", "board", "belt", "body", "plate", "base", "fixture",
                 "pole", "frame")
# Keys inside a node that are metadata, not child nodes to recurse into.
_NON_CHILD_KEYS = {"stack"}


def _is_light_spec(v):
    return isinstance(v, dict) and v.get("type") in _LIGHT_TYPES


def _subtree_has_buildable(v):
    if not isinstance(v, dict):
        return False
    if "primitive" in v or _is_light_spec(v):
        return True
    return any(_subtree_has_buildable(x) for x in v.values())


def _fmt_name(pattern, i, meta=None):
    if pattern is None:
        return None
    out = pattern
    if "{i}" in out:
        out = out.replace("{i}", str(i + 1))
    if meta:
        for k, val in meta.items():
            out = out.replace("{%s}" % k, str(val))
    return out


class SceneBuilder:
    def __init__(self, params, rules=None):
        self.params = params
        self.rules = rules or {}
        self.mat = MaterialEngine(params.get("material_library", {}))
        self.origin = Vector(params["station"]["world_position_m"])
        self.ctx = gb.BuildContext(self.mat, self.origin, self.rules)
        self.root = None

    # -- collection + root --------------------------------------------------
    def _make_collection(self):
        name = self.params["station"]["name"] + "_Build"
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
        layer = bpy.context.view_layer.layer_collection.children[coll.name]
        bpy.context.view_layer.active_layer_collection = layer
        self.ctx.collection = coll
        return coll

    def _make_root(self):
        conv = self.params.get("conventions", {})
        name = conv.get("root_object", self.params["station"]["name"] + "_Root")
        # The station root is always an empty; its display type is cosmetic.
        root = gb.create_empty(self.ctx, name, self.origin, etype="PLAIN_AXES")
        st = self.params["station"]
        root["unity_tag"] = "Station"
        root["station_id"] = st.get("id", "")
        root["station_type"] = st.get("type", "")
        self.root = root
        return root

    # -- position resolution ------------------------------------------------
    def _single_pos(self, node, parent):
        if "world_position_m" in node:
            return Vector(node["world_position_m"])
        if "offset_m" in node:
            return self.origin + Vector(node["offset_m"])
        if "offset_from_parent_m" in node and parent is not None:
            return parent.matrix_world @ Vector(node["offset_from_parent_m"])
        if "start_world_m" in node and "end_world_m" in node:
            return (Vector(node["start_world_m"]) + Vector(node["end_world_m"])) / 2.0
        return self.origin.copy()

    def _array_positions(self, node, count, parent, sib_offsets):
        if "offsets_m" in node:
            return [self.origin + Vector(o) for o in node["offsets_m"][:count]]
        if "start_offset_m" in node and "step_m" in node:
            s, st = Vector(node["start_offset_m"]), Vector(node["step_m"])
            return [self.origin + s + st * i for i in range(count)]
        if "stack" in node:
            return self._stack_positions(node, count)
        if sib_offsets and count in sib_offsets:
            base = [self.origin + Vector(o) for o in sib_offsets[count]]
            if "z_center_m" in node:
                for p in base:
                    p.z = float(node["z_center_m"])
            return base
        single = self._single_pos(node, parent)
        self.ctx.warnings.append("array node without layout; replicating single position")
        return [single.copy() for _ in range(count)]

    def _stack_positions(self, node, count):
        blk = node["stack"]
        grid = blk["grid_offsets_m"]
        base_z = float(blk.get("layer_base_z_m", 0.0))
        layer_h = float(blk.get("layer_height_m", 0.0))
        jitter = float(blk.get("layer_jitter_m", 0.0))
        cube = float(node.get("cube_size_m", 0.0))
        out = []
        for i in range(count):
            layer = i // len(grid)
            g = grid[i % len(grid)]
            j = jitter if layer else 0.0
            out.append(self.origin + Vector((g[0] + j, g[1] - j,
                       base_z + cube / 2.0 + layer * layer_h)))
        return out

    # -- node / container walk ---------------------------------------------
    def _sibling_offsets(self, items):
        pool = {}
        for _, v in items:
            offs = v.get("offsets_m") if isinstance(v, dict) else None
            if offs:
                pool[len(offs)] = offs
        return pool

    def _build_node(self, key, node, container_naming, parent, sib_offsets):
        primitive = node["primitive"]
        builder = registry.get_builder(primitive)
        if builder is None:
            self.ctx.warnings.append("unknown primitive '%s' -> box" % primitive)
            builder = registry.get_builder("box")

        naming = node.get("naming") or container_naming
        pattern = node.get("naming_pattern")
        rot = node.get("rotation_deg") or node.get("tilt_deg")
        mat_single = node.get("material")
        mat_cycle = node.get("material_cycle")
        count = node.get("count")

        built = []
        if count:
            positions = self._array_positions(node, count, parent, sib_offsets)
            for i in range(count):
                nm = _fmt_name(pattern or naming or key, i)
                mk = mat_cycle[i % len(mat_cycle)] if mat_cycle else mat_single
                obj = builder(self.ctx, nm, node, positions[i], rot, mk, parent)
                built.append(obj)
        else:
            pos = self._single_pos(node, parent)
            nm = naming or _fmt_name(pattern, 0) or key
            obj = builder(self.ctx, nm, node, pos, rot, mat_single, parent)
            built.append(obj)

        primary = built[0]
        # Recurse into nested child dicts (e.g. door, screen, button, segments).
        for ck, cv in node.items():
            if ck in _NON_CHILD_KEYS:
                continue
            if _is_light_spec(cv):
                self._build_light(ck, cv, primary)
            elif isinstance(cv, dict) and _subtree_has_buildable(cv):
                self._walk(ck, cv, None, primary)
        return primary

    def _build_items(self, node, parent):
        """Build a node that is a set of inline items (e.g. labels)."""
        pattern = node.get("naming_pattern")
        first = None
        for item in node["items"]:
            nm = _fmt_name(pattern, 0, {"name": item.get("name", "Item")}) \
                or item.get("name")
            pos = self._single_pos(item, parent)
            rot = item.get("rotation_deg") or _face_rotation(item.get("face"))
            obj = registry.get_builder("text")(self.ctx, nm, item, pos, rot,
                                               item.get("material"), parent)
            first = first or obj
        return first

    def _build_light(self, key, node, parent):
        nm = node.get("naming") or key
        pos = self._single_pos(node, parent)
        registry.get_builder("light")(self.ctx, nm, node, pos,
                                      node.get("rotation_deg"), None, parent)

    def _walk(self, key, spec, container_naming, parent, sib_offsets=None):
        if _is_light_spec(spec):
            self._build_light(key, spec, parent)
            return None
        if "primitive" in spec:
            # A node carrying an item list builds only its items (e.g. labels).
            if isinstance(spec.get("items"), list):
                return self._build_items(spec, parent)
            return self._build_node(key, spec, container_naming, parent, sib_offsets)
        # container
        items = [(k, v) for k, v in spec.items()
                 if isinstance(v, dict) and _subtree_has_buildable(v)]
        if not items:
            return None
        primary_key = _pick_primary(items)
        sib = self._sibling_offsets(items)
        repr_obj = None
        ordered = ([primary_key] if primary_key else []) + \
                  [k for k, _ in items if k != primary_key]
        as_dict = dict(items)
        for k in ordered:
            cn = spec.get("naming") if k == primary_key else None
            attach = parent if repr_obj is None else repr_obj
            r = self._walk(k, as_dict[k], cn, attach, sib)
            if k == primary_key:
                repr_obj = r
        return repr_obj

    # -- public -------------------------------------------------------------
    def build(self):
        self._make_collection()
        self._make_root()
        for key, comp in self.params.get("components", {}).items():
            self._walk(key, comp, None, self.root)
        return self.ctx.objects, self.root


def _pick_primary(items):
    # 1) explicit marker wins ( "primary": true on a child node )
    for k, v in items:
        if isinstance(v, dict) and v.get("primary") is True:
            return k
    # 2) generic component-role hint
    keys = [k for k, _ in items]
    for pk in _PRIMARY_KEYS:
        if pk in keys:
            return pk
    # 3) else first item that is a primitive node
    for k, v in items:
        if "primitive" in v:
            return k
    return keys[0] if keys else None


def _face_rotation(face):
    # A text mesh's readable normal is +Z by default. These rotations turn it
    # to face the requested world axis (readable from that side).
    if face == "+Y":
        return [90.0, 0.0, 180.0]
    if face == "-Y":
        return [90.0, 0.0, 0.0]
    if face == "+Z":
        return [0.0, 0.0, 0.0]
    return [0.0, 0.0, 0.0]
