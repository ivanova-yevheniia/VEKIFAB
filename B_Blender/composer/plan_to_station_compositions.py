"""
plan_to_station_compositions.py — one composition per positioned station instance.

Input:  requirements/factory_description.json
        assets/asset_registry.json
Output: composer/station_compositions/<id>_<type>_composition.json   (one per instance)
        composer/factory_composition.json                            (regenerated index)
        review/review_rules.json                                     (line ids synced)

Chooses asset instances per station type using ONLY assets present in the registry,
with consistent STATION_/INFO_/TRIGGER_/COLLIDER_/PHYS_ naming and Unity metadata.

Standard library only. Deterministic. No Blender.
"""

import os
import sys
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_B_ROOT = os.path.dirname(_HERE)
_REQ = os.path.join(_B_ROOT, "requirements")
_SC = os.path.join(_HERE, "station_compositions")

SHORT = {
    "loading_station": "Loading", "assisted_assembly_station": "Assembly",
    "robot_handling_cell": "RobotCell", "vision_inspection_station": "Vision",
    "functional_test_station": "FunctionalTest", "packaging_station": "Packaging",
    "finished_goods_storage": "Storage",
}
BASENAME = {
    "loading_station": "loading_station", "assisted_assembly_station": "assembly_station",
    "robot_handling_cell": "robot_cell", "vision_inspection_station": "vision_inspection",
    "functional_test_station": "functional_test_station", "packaging_station": "packaging_station",
    "finished_goods_storage": "storage_station",
}
MANNED = {"loading_station", "assisted_assembly_station", "robot_handling_cell",
          "vision_inspection_station", "functional_test_station", "packaging_station"}


def load_json(p):
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


class Composer:
    def __init__(self):
        self.reg = load_json(os.path.join(_B_ROOT, "assets", "asset_registry.json"))
        self.asset_ids = {a["id"] for a in self.reg["assets"]}

    def _use(self, aid):
        if aid not in self.asset_ids:
            raise RuntimeError("asset '%s' not in registry" % aid)
        return aid

    def _inst(self, sid, nn, short, aid, key, idx, pos, suffix, tags, role, ov=None, sockets=None):
        self._use(aid)
        if aid == "information_panel":
            name = "INFO_%s_Panel" % short
        elif aid == "roller_conveyor":
            name = "CONVEYOR_%s_%s" % (short, suffix)
        elif aid == "cardboard_box":
            name = "PHYS_%s_Box_%d" % (short, idx)
        elif aid.startswith("robot_"):
            name = "PHYS_%s_%s" % (short, suffix)
        else:
            name = "STATION_%s_%s_%s" % (nn, short, suffix)
        return {
            "instance_id": "%s_%s_%d" % (sid, key, idx), "asset_id": aid,
            "position": [round(pos[0], 3), round(pos[1], 3), round(pos[2], 3)],
            "rotation": [0, 0, 0], "scale": 1.0, "parameter_overrides": ov or {},
            "name_prefix": name, "socket_connections": sockets or [], "unity_tags": tags,
            "physics_role": role,
        }

    def bill(self, st, has_in, has_out):
        t = st["type"]
        short = SHORT[t]
        sid = st["id"]
        nn = "".join(ch for ch in sid if ch.isdigit()) or sid
        out = []

        def add(aid, key, idx, pos, suffix, tags, role, ov=None, sockets=None):
            out.append(self._inst(sid, nn, short, aid, key, idx, pos, suffix, tags, role, ov, sockets))

        # frame + feet
        corners = [(-0.8, -0.6), (0.8, -0.6), (-0.8, 0.6), (0.8, 0.6)]
        for i, (x, y) in enumerate(corners, 1):
            add("aluminium_profile", "leg", i, [x, y, 0.43], "Leg_%d" % i, ["Frame"], "static",
                {"length_m": 0.86})
        for i, (x, y) in enumerate(corners, 1):
            add("adjustable_foot", "foot", i, [x, y, 0.0], "Foot_%d" % i, ["Foot"], "static")
        # info panel (every station)
        add("information_panel", "info", 1, [0.0, 2.4, 0.0], "Panel", ["InfoPanel", "Trigger"],
            "trigger", {"board_height_m": 1.6})
        # status light (safety asset on every station)
        add("stack_light", "stack", 1, [0.9, -0.8, 1.9], "StackLight", ["StackLight"], "static")
        # conveyors
        if has_in:
            add("roller_conveyor", "conv_in", 1, [-1.9, 0.0, 0.4], "Input", ["Conveyor"], "kinematic")
        if has_out:
            add("roller_conveyor", "conv_out", 1, [1.9, 0.0, 0.4], "Output", ["Conveyor"], "kinematic")
        # manned controls
        if t in MANNED:
            add("emergency_stop", "estop", 1, [-1.05, -0.7, 1.15], "EStop", ["EmergencyStop"], "static")
            add("electrical_cabinet", "cabinet", 1, [-1.2, -0.5, 0.4], "Cabinet", ["Cabinet"], "static")
            add("task_light", "task", 1, [0.0, -0.55, 2.15], "TaskLight", ["TaskLight"], "static")

        # type-specific
        if t == "loading_station":
            for i, dx in enumerate((-0.6, -0.3, 0.0, 0.3), 1):
                add("plastic_parts_bin", "bin", i, [dx, -0.75, 1.0], "Bin_%d" % i, ["Bin"], "static")
            for i, dx in enumerate((-0.4, 0.5), 1):
                add("pallet", "pallet", i, [dx, 0.6, 0.06], "Pallet_%d" % i, ["Pallet"], "static")
            for i in range(1, 5):
                add("cardboard_box", "box", i, [-0.2 + 0.35 * ((i - 1) % 2), -0.5 + 0.35 * ((i - 1) // 2), 0.95],
                    "Box_%d" % i, ["Box"], "dynamic", {"mass_kg": 0.6})
            add("cable_chain", "cable", 1, [-1.0, -0.8, 0.8], "CableChain", ["CableChain"], "static")
        elif t == "assisted_assembly_station":
            for i, dx in enumerate((-0.6, -0.3, 0.0, 0.3), 1):
                add("plastic_parts_bin", "bin", i, [dx, -0.75, 1.0], "Bin_%d" % i, ["Bin"], "static")
            add("hmi_panel", "hmi", 1, [0.85, -0.5, 1.3], "HMI", ["HMI"], "static")
            for i in range(1, 3):
                add("cardboard_box", "box", i, [-0.2 + 0.35 * (i - 1), -0.5, 0.95], "Box_%d" % i,
                    ["Box"], "dynamic", {"mass_kg": 0.6})
        elif t == "robot_handling_cell":
            for aid, key, sfx in [("robot_pedestal", "ped", "Pedestal"), ("robot_base", "rbase", "Base"),
                                  ("robot_arm", "arm", "Arm"), ("robot_gripper", "grip", "Gripper")]:
                add(aid, key, 1, [0.0, -0.45, 0.0], sfx, ["Robot"], "kinematic")
            add("safety_fence", "fence", 1, [0.0, 0.0, 0.0], "Fence", ["SafetyFence"], "static",
                {"bay_width_m": 2.7})
            add("hmi_panel", "hmi", 1, [0.7, 1.6, 1.3], "HMI", ["HMI"], "static")
            add("barcode_scanner", "scanner", 1, [0.0, -0.5, 1.4], "Scanner", ["Sensor"], "static")
            add("cable_chain", "cable", 1, [0.0, -1.1, 0.1], "CableChain", ["CableChain"], "static")
        elif t == "vision_inspection_station":
            add("barcode_scanner", "scanner", 1, [0.0, -0.5, 1.5], "Scanner", ["Sensor"], "static")
            add("hmi_panel", "hmi", 1, [0.85, -0.5, 1.3], "HMI", ["HMI"], "static")
        elif t == "functional_test_station":
            add("barcode_scanner", "scanner", 1, [0.3, -0.5, 1.4], "Scanner", ["Sensor"], "static")
            add("hmi_panel", "hmi", 1, [0.85, -0.5, 1.3], "HMI", ["HMI"], "static")
            add("cardboard_box", "box", 1, [0.0, -0.5, 0.95], "Box_1", ["Box"], "dynamic", {"mass_kg": 0.6})
        elif t == "packaging_station":
            for i in range(1, 5):
                add("cardboard_box", "box", i, [-0.2 + 0.35 * ((i - 1) % 2), -0.5 + 0.35 * ((i - 1) // 2), 0.95],
                    "Box_%d" % i, ["Box"], "dynamic", {"mass_kg": 0.6})
            add("pallet", "pallet", 1, [0.5, 0.6, 0.06], "Pallet_1", ["Pallet"], "static")
            add("hmi_panel", "hmi", 1, [0.85, -0.5, 1.3], "HMI", ["HMI"], "static")
        elif t == "finished_goods_storage":
            for i in range(1, 5):
                add("pallet", "pallet", i, [-0.6 + 0.9 * ((i - 1) % 2), 0.5 * ((i - 1) // 2), 0.06],
                    "Pallet_%d" % i, ["Pallet"], "static")
            for i in range(1, 9):
                add("cardboard_box", "box", i, [-0.5 + 0.35 * ((i - 1) % 3), -0.3 + 0.35 * ((i - 1) // 3), 0.95],
                    "Box_%d" % i, ["Box"], "dynamic", {"mass_kg": 0.6})
        return out


def main():
    fd = load_json(os.path.join(_REQ, "factory_description.json"))
    comp = Composer()
    os.makedirs(_SC, exist_ok=True)

    has_in = {c["to"] for c in fd["conveyors"]}
    has_out = {c["from"] for c in fd["conveyors"]}

    station_index = []
    for st in fd["stations"]:
        instances = comp.bill(st, st["id"] in has_in, st["id"] in has_out)
        dims = st["dimensions_m"]
        cdoc = {
            "schema_version": "1.0",
            "station": {"id": st["id"], "type": st["type"], "name": st["name"],
                        "world_position_m": st["position"],
                        "envelope_m": dims, "front_axis": "+Y", "flow_axis": "+X"},
            "instances": instances,
        }
        fname = "%s_%s_composition.json" % (st["id"], SHORT[st["type"]].lower())
        json.dump(cdoc, open(os.path.join(_SC, fname), "w", encoding="utf-8"), indent=2)
        station_index.append({
            "id": st["id"], "type": st["type"], "name": st["name"],
            "world_position_m": st["position"], "envelope_m": dims,
            "composition_file": "station_compositions/" + fname, "instance_count": len(instances),
        })

    # regenerate the composer index (so review/report see the new line)
    factory = {
        "schema_version": "1.0",
        "project": {"name": "VEKIFAB — AI Factory Planner",
                    "work_package": "WP B — Blender station prefab generation",
                    "use_case": "Planner-driven line; Unity assembles the walkthrough",
                    "product": fd["scene"].get("product", ""), "line": fd["scene"].get("name", "")},
        "units": "meters",
        "factory_floor": {"size_m": fd["factory_floor"]["size_m"], "origin": [0.0, 0.0, 0.0]},
        "asset_library": "assets/asset_registry.json",
        "stations": station_index,
        "conveyors": [{"id": c["id"], "name": c["name"], "from": c["from"], "to": c["to"],
                       "start_m": c["start"], "end_m": c["end"], "width_m": c.get("width_m", 0.6)}
                      for c in fd["conveyors"]],
        "avatar_walkway": {"name": fd["avatar_walkway"]["name"], "width_m": fd["avatar_walkway"]["width_m"],
                           "waypoints_m": [w["position"] for w in fd["avatar_walkway"]["waypoints"]]},
        "info_panels": [{"id": ip["id"], "station": ip["station"], "name": ip["name"],
                         "position_m": ip["position"]} for ip in fd["info_panels"]],
        "safety_zones": [{"id": z["id"], "name": z["name"], "station": z["station"], "type": z["type"],
                          "area_min_m": z["area_min"], "area_max_m": z["area_max"], "height_m": z["height_m"]}
                         for z in fd["safety_zones"]],
        "export": {"blend_dir": "exports/blend", "glb_dir": "exports/glb",
                   "screenshots_dir": "exports/screenshots",
                   "station_basenames": {st["id"]: BASENAME[st["type"]] for st in fd["stations"]}},
    }
    json.dump(factory, open(os.path.join(_HERE, "factory_composition.json"), "w", encoding="utf-8"), indent=2)

    # sync review rules to the new line ids (data-only; review code unchanged)
    main_path, seen = [], set()
    for st in fd["stations"]:
        grp = st.get("parallel_group")
        key = grp or st["id"]
        if key not in seen:
            seen.add(key)
            main_path.append(st["id"])
    rr_path = os.path.join(_B_ROOT, "review", "review_rules.json")
    rr = load_json(rr_path)
    rr["station_order"] = main_path
    rr["flow_start"] = main_path[0]
    rr["flow_end"] = main_path[-1]
    rr["emergency_stop_required_stations"] = [st["id"] for st in fd["stations"] if st["type"] in MANNED]
    json.dump(rr, open(rr_path, "w", encoding="utf-8"), indent=2)

    par = sum(1 for st in fd["stations"] if st.get("parallel_group"))
    print("station compositions: %d files (%d parallel instances)" % (len(station_index), par))
    print("regenerated composer/factory_composition.json and synced review/review_rules.json")


if __name__ == "__main__":
    main()
