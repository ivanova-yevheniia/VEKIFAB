"""
assembly_engine.py — Generic assembly / hierarchy resolver.

Reads an assembly specification (ordered build operations with a dependency
graph) and:
  * resolves a valid build order (topological sort of `dependencies`),
  * attaches each operation's sub-assembly to its declared `parent`.

The scene builder already created every object and did the *intra*-component
parenting. This engine performs the *cross*-component attachment: for each
operation it parents the operation's primary object (its first child) to the
operation's `parent` object, preserving world transform.

Nothing here is station-specific — it only understands operations, names and
patterns.
"""

import geometry_builder as gb


def topo_sort(operations):
    """Return operation dicts ordered so every dependency precedes its dependent.

    Raises ValueError on a dependency cycle.
    """
    by_id = {op["operation_id"]: op for op in operations}
    visited, done, order = set(), set(), []

    def visit(op_id, stack):
        if op_id in done:
            return
        if op_id in stack:
            raise ValueError("dependency cycle at operation '%s'" % op_id)
        stack.add(op_id)
        for dep in by_id.get(op_id, {}).get("dependencies", []):
            if dep in by_id:
                visit(dep, stack)
        stack.discard(op_id)
        done.add(op_id)
        order.append(by_id[op_id])

    for op in operations:
        visit(op["operation_id"], set())
    return order


def expand_pattern(name, objects):
    """Expand a child reference into concrete object names present in `objects`.

    Supports:
      * "NAME"          -> ["NAME"] if present
      * "NAME_1..4"     -> ["NAME_1", ... "NAME_4"]
      * "NAME_*"        -> every object whose name starts with "NAME_"
    """
    if name is None:
        return []
    if ".." in name:
        head, rng = name.rsplit("_", 1)
        try:
            lo, hi = rng.split("..")
            return ["%s_%d" % (head, i) for i in range(int(lo), int(hi) + 1)
                    if ("%s_%d" % (head, i)) in objects]
        except ValueError:
            pass
    if name.endswith("_*"):
        prefix = name[:-1]  # keep trailing underscore
        return [n for n in objects if n.startswith(prefix)]
    return [name] if name in objects else []


def apply_hierarchy(operations, objects):
    """Attach each operation's primary object to its declared parent object.

    Returns a list of warning strings for unresolved references.
    """
    warnings = []
    order = topo_sort(operations)
    for op in order:
        parent_name = op.get("parent")
        children = op.get("children", []) or []
        if not parent_name or not children:
            continue
        parent_obj = objects.get(parent_name)
        if parent_obj is None:
            warnings.append("op %s: parent '%s' not found"
                            % (op["operation_id"], parent_name))
            continue
        # Primary = first resolvable object of the first child reference.
        primary_objs = expand_pattern(children[0], objects)
        if not primary_objs:
            warnings.append("op %s: primary child '%s' not found"
                            % (op["operation_id"], children[0]))
            continue
        primary = objects[primary_objs[0]]
        if primary is parent_obj:
            continue
        gb.parent_keep(primary, parent_obj)
    return warnings
