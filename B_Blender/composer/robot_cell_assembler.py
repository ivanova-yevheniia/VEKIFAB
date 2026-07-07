"""
robot_cell_assembler.py — Instantiate robot assets into a kinematic robot.

Reads a station source spec whose `robot` component is an *asset_composition*
placeholder (no geometry), loads the RobotPedestal / RobotBase / RobotArm /
RobotGripper assets from the asset library, and composes them into a single
kinematic parent chain:

    Pedestal -> Base -> Waist -> Shoulder -> Upper Arm -> Elbow -> Forearm
             -> Wrist -> Gripper -> (product)

It then writes the resolved `robot_cell_parameters.json` + `robot_cell_assembly.json`
that the procedural builder renders. No bespoke robot geometry lives in the
station source — geometry comes only from the assets. Standard library only.
Deterministic.
"""

import os
import sys
import json
import copy

_HERE = os.path.dirname(os.path.abspath(__file__))
_B_ROOT = os.path.dirname(_HERE)
_ASSETS = os.path.join(_B_ROOT, "assets")
_PS = os.path.join(_B_ROOT, "parametric_specs")

# role (from asset component nodes) -> station object name
ROLE_NAME = {
    "pedestal": "COLLIDER_RobotCell_Pedestal",
    "base": "PHYS_RobotCell_Base", "flange": "PHYS_RobotCell_Flange",
    "waist": "PHYS_RobotCell_Waist", "shoulder": "PHYS_RobotCell_Shoulder",
    "upper_arm": "PHYS_RobotCell_UpperArm", "elbow": "PHYS_RobotCell_Elbow",
    "forearm": "PHYS_RobotCell_Forearm", "wrist": "PHYS_RobotCell_Wrist",
    "gripper": "PHYS_RobotCell_Gripper", "finger_a": "PHYS_RobotCell_FingerA",
    "finger_b": "PHYS_RobotCell_FingerB", "product": "PHYS_RobotCell_Pump",
    "product_screen": "PHYS_RobotCell_PumpScreen",
}


def load_json(p):
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _registry_folder():
    reg = load_json(os.path.join(_ASSETS, "asset_registry.json"))
    return {a["id"]: a["folder"] for a in reg["assets"]}


def load_asset(asset_id, folders):
    d = os.path.join(_ASSETS, folders[asset_id])
    return load_json(os.path.join(d, "parameters.json")), load_json(os.path.join(d, "builder.json"))


def find_by_role(node, role):
    if isinstance(node, dict):
        if node.get("role") == role:
            return node
        for v in node.values():
            if isinstance(v, dict):
                r = find_by_role(v, role)
                if r is not None:
                    return r
    return None


def rename_and_strip(node):
    """Apply ROLE_NAME to every roled node and remove the helper 'role' key."""
    if isinstance(node, dict):
        role = node.get("role")
        if role in ROLE_NAME:
            node["naming"] = ROLE_NAME[role]
        node.pop("role", None)
        for v in node.values():
            rename_and_strip(v)
    return node


def collect_materials(node, acc):
    if isinstance(node, dict):
        if node.get("material"):
            acc.add(node["material"])
        for m in node.get("material_cycle", []) or []:
            acc.add(m)
        for v in node.values():
            collect_materials(v, acc)
    return acc


def build_pump():
    return {
        "role": "product", "primitive": "box", "dimensions_m": [0.10, 0.07, 0.04],
        "offset_from_parent_m": [0.0, 0.0, -0.16], "bevel_m": 0.006,
        "material": "white_panel", "unity_tag": "PumpPart",
        "screen": {"role": "product_screen", "primitive": "box",
                   "dimensions_m": [0.05, 0.004, 0.02],
                   "offset_from_parent_m": [0.0, -0.036, 0.006], "material": "screen_dark"},
    }


def assemble_robot(spec, folders):
    comp = spec["components"]["robot"]["asset_composition"]
    chain = comp["chain"]
    mount = comp.get("mount_m", [0, 0, 0])

    ped_p, ped_b = load_asset(chain[0], folders)
    robot = copy.deepcopy(ped_p["components"][ped_b["assembler"]["entry_key"]])
    base_off = robot.get("offset_m", [0, 0, 0])
    robot["offset_m"] = [mount[0] + base_off[0], mount[1] + base_off[1], base_off[2]]
    robot["primary"] = True

    prev_b = ped_b
    for i, aid in enumerate(chain[1:], start=1):
        ap, ab = load_asset(aid, folders)
        node = copy.deepcopy(ap["components"][ab["assembler"]["entry_key"]])
        node.pop("offset_m", None)
        node["offset_from_parent_m"] = ab["assembler"]["join_offset_m"]
        target = find_by_role(robot, prev_b["assembler"]["tool_node"])
        if target is None:
            raise RuntimeError("attach role '%s' not found for %s"
                               % (prev_b["assembler"]["tool_node"], aid))
        target["_link_%d" % i] = node
        prev_b = ab

    # product in the gripper (visible handling task)
    if comp.get("product", {}).get("in_gripper"):
        grip = find_by_role(robot, prev_b["assembler"]["tool_node"])
        grip["_product"] = build_pump()

    rename_and_strip(robot)
    return robot


PRIMARY_KEYS = ("worktop", "board", "belt", "body", "plate", "base", "fixture", "pole", "frame")


def resolve_primary(spec):
    if isinstance(spec, dict) and "primitive" in spec:
        if isinstance(spec.get("items"), list):
            it = spec["items"][0]
            return spec.get("naming_pattern", "").replace("{name}", str(it.get("name", "")))
        if spec.get("count") and spec.get("naming_pattern"):
            return spec["naming_pattern"].replace("{i}", "1")
        return spec.get("naming") or spec.get("naming_pattern", "").replace("{i}", "1")
    if isinstance(spec, dict):
        for k, v in spec.items():
            if isinstance(v, dict) and v.get("primary") is True:
                return resolve_primary(v)
        for pk in PRIMARY_KEYS:
            if pk in spec and isinstance(spec[pk], dict):
                return resolve_primary(spec[pk])
        for v in spec.values():
            if isinstance(v, dict) and ("primitive" in v or any(isinstance(x, dict) for x in v.values())):
                return resolve_primary(v)
    return None


PALETTE = None


def _palette():
    global PALETTE
    if PALETTE is None:
        PALETTE = {}
        for f in ("robot_cell_parameters.json",):
            pass
        # pull PBR defs from an existing robot asset (they share the canonical palette)
        for aid in ("robot_arm", "robot_base", "robot_gripper", "robot_pedestal"):
            folders = _registry_folder()
            ap, _ = load_asset(aid, folders)
            PALETTE.update(ap.get("material_library", {}))
    return PALETTE


def main():
    folders = _registry_folder()
    spec = load_json(os.path.join(_PS, "robot_cell_station.json"))

    robot = assemble_robot(spec, folders)
    spec["components"]["robot"] = robot

    # union materials used by the robot into the station material_library
    used = collect_materials(robot, set())
    pal = _palette()
    for m in used:
        if m not in spec["material_library"] and m in pal:
            spec["material_library"][m] = pal[m]

    # regenerate assembly from the resolved components
    root = spec["conventions"]["root_object"]
    ops = [{"operation_id": "op_010_root", "parent": None, "children": [root],
            "geometry": {"primitive": "empty", "at": "station.world_position_m"},
            "dependencies": [], "required_materials": [], "estimated_complexity": "trivial"}]
    i = 2
    for key, node in spec["components"].items():
        prim = resolve_primary(node)
        ops.append({"operation_id": "op_%03d_%s" % (i * 10, key), "parent": root,
                    "children": [prim] if prim else [],
                    "geometry": {"source": "components.%s" % key},
                    "dependencies": ["op_010_root"], "required_materials": [],
                    "estimated_complexity": "high" if key == "robot" else "low"})
        i += 1
    ops.append({"operation_id": "op_999_finalize", "parent": None, "children": [],
                "geometry": {"action": "apply_unity_tags_and_export"},
                "dependencies": [o["operation_id"] for o in ops[1:]],
                "required_materials": [], "estimated_complexity": "low"})
    assembly = {"schema_version": "1.0", "station": "S03", "type": "robot_handling_cell",
                "parameters_ref": "robot_cell_parameters.json", "operations": ops}

    json.dump(spec, open(os.path.join(_PS, "robot_cell_parameters.json"), "w", encoding="utf-8"), indent=2)
    json.dump(assembly, open(os.path.join(_PS, "robot_cell_assembly.json"), "w", encoding="utf-8"), indent=2)

    # report the resolved kinematic chain
    chain = []

    def walk(n, depth):
        if isinstance(n, dict):
            if n.get("naming", "").startswith(("PHYS_RobotCell", "COLLIDER_RobotCell")):
                chain.append("  " * depth + n["naming"])
            for v in n.values():
                if isinstance(v, dict):
                    walk(v, depth + 1)
    walk(robot, 0)
    print("Robot cell assembler:")
    print("  instantiated assets:", " -> ".join(spec["components"]["robot"].get("naming", "") and
          ["robot_pedestal", "robot_base", "robot_arm", "robot_gripper"]))
    print("  kinematic hierarchy:")
    for c in chain:
        print("   ", c)
    print("  wrote robot_cell_parameters.json + robot_cell_assembly.json")


if __name__ == "__main__":
    main()
