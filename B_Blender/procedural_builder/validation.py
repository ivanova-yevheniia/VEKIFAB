"""
validation.py — Specification & built-scene validation for the procedural builder.

Static checks (no Blender required) run on the parsed JSON:
  * unknown component types
  * missing materials (referenced but not in the library)
  * duplicate object names
  * missing dependencies (assembly deps referencing absent operations)
  * parent loops (assembly parent/child cycles)
  * invalid hierarchy (operation parenting to its own descendant)

Runtime checks (require Blender) run on the built objects:
  * missing transforms
  * duplicate names
  * overlapping bounding boxes

Everything is generic — no station knowledge.
"""

try:
    import bpy
    _HAS_BPY = True
except ImportError:
    bpy = None
    _HAS_BPY = False


class Issue:
    def __init__(self, severity, code, message):
        self.severity = severity      # "error" | "warning"
        self.code = code
        self.message = message

    def __repr__(self):
        return "[%s] %s: %s" % (self.severity.upper(), self.code, self.message)


class Report:
    def __init__(self):
        self.issues = []

    def add(self, severity, code, message):
        self.issues.append(Issue(severity, code, message))

    def error(self, code, message):
        self.add("error", code, message)

    def warning(self, code, message):
        self.add("warning", code, message)

    @property
    def errors(self):
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self):
        return [i for i in self.issues if i.severity == "warning"]

    def ok(self):
        return not self.errors

    def summary(self):
        return "%d error(s), %d warning(s)" % (len(self.errors), len(self.warnings))


# ---------------------------------------------------------------------------
# Static spec walk helpers
# ---------------------------------------------------------------------------

_LIGHT_TYPES = {"AREA", "POINT", "SUN", "SPOT"}


def _iter_nodes(spec):
    """Yield every dict that is a buildable node (has 'primitive' or is a light)."""
    if isinstance(spec, dict):
        if "primitive" in spec or spec.get("type") in _LIGHT_TYPES:
            yield spec
        for v in spec.values():
            yield from _iter_nodes(v)
    elif isinstance(spec, list):
        for v in spec:
            yield from _iter_nodes(v)


def _resolved_names(spec):
    """Best-effort enumeration of object names a node will produce."""
    names = []
    for node in _iter_nodes(spec):
        count = node.get("count")
        naming = node.get("naming")
        pattern = node.get("naming_pattern")
        if count and pattern:
            names += [pattern.replace("{i}", str(i + 1)) for i in range(count)]
        elif count and naming:
            names += [naming] * count
        elif naming:
            names.append(naming)
        elif pattern and "{i}" in pattern:
            names.append(pattern.replace("{i}", "1"))
        for item in node.get("items", []) if isinstance(node.get("items"), list) else []:
            if pattern:
                names.append(pattern.replace("{name}", str(item.get("name", ""))))
    return names


def _material_refs(spec):
    refs = set()
    for node in _iter_nodes(spec):
        if node.get("material"):
            refs.add(node["material"])
        for m in node.get("material_cycle", []) or []:
            refs.add(m)
    if isinstance(spec, dict):
        for v in spec.values():
            if isinstance(v, (dict, list)):
                refs |= _material_refs(v)
    elif isinstance(spec, list):
        for v in spec:
            refs |= _material_refs(v)
    return refs


# ---------------------------------------------------------------------------
# Static validation
# ---------------------------------------------------------------------------

def validate_specs(params, assembly=None, known_types=None, report=None):
    report = report or Report()
    components = params.get("components", {})
    library = set(params.get("material_library", {}).keys())

    # unknown component types
    if known_types is not None:
        for node in _iter_nodes(components):
            t = node.get("primitive") or node.get("type")
            if t and t not in known_types and t not in _LIGHT_TYPES:
                report.error("unknown_component_type",
                             "component type '%s' has no registered builder" % t)

    # missing materials
    for ref in _material_refs(components):
        if ref not in library:
            report.error("missing_material",
                         "material '%s' referenced but not in material_library" % ref)

    # duplicate names
    names = _resolved_names(components)
    seen, dup = set(), set()
    for n in names:
        if n in seen:
            dup.add(n)
        seen.add(n)
    for n in sorted(dup):
        report.warning("duplicate_name", "object name '%s' produced more than once" % n)

    # missing transforms (a node must resolve to some position)
    for node in _iter_nodes(components):
        if node.get("type") in _LIGHT_TYPES:
            continue
        pos_keys = ("world_position_m", "offset_m", "offset_from_parent_m",
                    "offsets_m", "start_offset_m", "start_world_m", "stack")
        if not any(k in node for k in pos_keys) and "items" not in node:
            report.warning("missing_transform",
                           "node '%s' has no position field" % node.get("naming",
                           node.get("naming_pattern", node.get("primitive", "?"))))

    if assembly:
        _validate_assembly(assembly, report)
    return report


def _validate_assembly(assembly, report):
    ops = assembly.get("operations", [])
    ids = {op["operation_id"] for op in ops}

    # missing dependencies
    for op in ops:
        for dep in op.get("dependencies", []):
            if dep not in ids:
                report.error("missing_dependency",
                             "op '%s' depends on missing op '%s'"
                             % (op["operation_id"], dep))

    # dependency cycles
    color = {}

    def dfs(oid, by_id):
        color[oid] = 1
        for dep in by_id.get(oid, {}).get("dependencies", []):
            if dep not in by_id:
                continue
            if color.get(dep) == 1:
                report.error("parent_loop",
                             "dependency cycle through '%s' -> '%s'" % (oid, dep))
                return
            if color.get(dep, 0) == 0:
                dfs(dep, by_id)
        color[oid] = 2

    by_id = {op["operation_id"]: op for op in ops}
    for op in ops:
        if color.get(op["operation_id"], 0) == 0:
            dfs(op["operation_id"], by_id)

    # invalid hierarchy: an op whose parent name equals one of its own children
    for op in ops:
        parent = op.get("parent")
        if parent and parent in (op.get("children") or []):
            report.error("invalid_hierarchy",
                         "op '%s' parents to its own child '%s'"
                         % (op["operation_id"], parent))


# ---------------------------------------------------------------------------
# Runtime validation (requires Blender objects)
# ---------------------------------------------------------------------------

def _world_aabb(obj):
    corners = [obj.matrix_world @ __v(c) for c in obj.bound_box]
    xs = [c.x for c in corners]
    ys = [c.y for c in corners]
    zs = [c.z for c in corners]
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def __v(c):
    from mathutils import Vector
    return Vector((c[0], c[1], c[2]))


def _overlap(a, b, gap=0.0):
    (amin, amax), (bmin, bmax) = a, b
    for i in range(3):
        if amax[i] <= bmin[i] + gap or bmax[i] <= amin[i] + gap:
            return False
    return True


def validate_built(objects, constraints=None, report=None):
    report = report or Report()
    if not _HAS_BPY:
        report.warning("no_bpy", "runtime validation skipped (Blender not available)")
        return report

    # duplicate names in the actual scene
    seen = {}
    for name, obj in objects.items():
        if obj is None:
            report.error("missing_object", "object '%s' was not built" % name)
            continue
        seen.setdefault(obj.name, 0)
        seen[obj.name] += 1
        # missing transforms
        if obj.matrix_world is None or obj.location is None:
            report.error("missing_transform", "object '%s' has no transform" % name)
    for n, c in seen.items():
        if c > 1:
            report.warning("duplicate_name", "name '%s' appears %d times" % (n, c))

    # parent loops in the built hierarchy
    for name, obj in objects.items():
        if obj is None:
            continue
        seen_chain, p = set(), obj
        while p is not None:
            if p.name in seen_chain:
                report.error("parent_loop", "parent loop involving '%s'" % obj.name)
                break
            seen_chain.add(p.name)
            p = p.parent

    # Overlapping bounding boxes among solid parts that should not intersect.
    # Skipped generically (no station-specific names): non-meshes, triggers,
    # anything tagged as floor, flat markings/decals (thin in Z), and nested
    # parts (only top-level solids are compared, to limit noise).
    def _skip(o):
        if o is None or o.type != "MESH" or o.parent is not None:
            return True
        if o.get("is_trigger") or o.get("unity_tag") in ("Floor", "FloorMarking"):
            return True
        (_, _, zmin), (_, _, zmax) = _world_aabb(o)
        return (zmax - zmin) < 0.05   # flat floor marking / decal

    meshes = [o for o in objects.values() if not _skip(o)]
    gap = 0.0
    if constraints:
        gap = -abs(constraints.get("minimum_clearances", {})
                   .get("component_to_component_gap_m", 0.0))
    boxes = [(o.name, _world_aabb(o)) for o in meshes]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if _overlap(boxes[i][1], boxes[j][1], gap):
                report.warning("bbox_overlap",
                               "bounding boxes overlap: '%s' & '%s'"
                               % (boxes[i][0], boxes[j][0]))
    return report
