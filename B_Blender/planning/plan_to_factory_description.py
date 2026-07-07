"""
plan_to_factory_description.py — turn a planned line into positioned instances.

Input:  requirements/production_line_plan.json  (from planner.py)
Output: requirements/factory_description.json

Converts planned process steps into positioned station instances, expands
parallel assembly (parallel_units > 1) into multiple instances, links conveyors,
builds the avatar walkway, info-panel positions and trigger names, and keeps every
coordinate inside available_area_m. Station ids and types are preserved.

Standard library only. Deterministic. No Blender.
"""

import os
import sys
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_B_ROOT = os.path.dirname(_HERE)
_REQ = os.path.join(_B_ROOT, "requirements")

SHORT = {
    "loading_station": "Loading", "assisted_assembly_station": "Assembly",
    "robot_handling_cell": "RobotCell", "vision_inspection_station": "Vision",
    "functional_test_station": "FunctionalTest", "packaging_station": "Packaging",
    "finished_goods_storage": "Storage",
}
PREFAB = {
    "loading_station": "loading_station.glb", "assisted_assembly_station": "assembly_station.glb",
    "robot_handling_cell": "robot_cell.glb", "vision_inspection_station": "vision_inspection.glb",
    "functional_test_station": "functional_test_station.glb", "packaging_station": "packaging_station.glb",
    "finished_goods_storage": "storage_station.glb",
}
# reasoning_summary.json is keyed by the canonical process position
REASON = {
    "loading_station": "S01", "assisted_assembly_station": "S02", "robot_handling_cell": "S03",
    "vision_inspection_station": "S04", "functional_test_station": "S05",
    "packaging_station": "S06", "finished_goods_storage": "S07",
}
DIMS = {
    "loading_station": (2.0, 2.0, 2.0), "assisted_assembly_station": (2.5, 2.0, 2.0),
    "robot_handling_cell": (3.0, 3.0, 2.5), "vision_inspection_station": (2.0, 2.0, 2.5),
    "functional_test_station": (2.0, 2.0, 2.0), "packaging_station": (2.5, 2.0, 2.0),
    "finished_goods_storage": (3.5, 3.5, 3.0),
}


def load_json(p):
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def build(plan):
    pl = plan.get("planner", {})
    area = pl.get("available_area_m", {"length_x": 25.0, "width_y": 18.0})
    LX = float(area.get("length_x") or 25.0)
    WY = float(area.get("width_y") or 18.0)
    margin = min(2.5, LX * 0.1)
    line_y = round(WY * 0.34, 2)
    walkway_y = round(WY * 0.58, 2)
    par_offset = 2.6  # full separation between adjacent parallel instances (clears footprints)

    # slots = one x-position per process step; parallel assembly expands within a slot
    slots = []
    for ps in plan["stations"]:
        n = ps.get("parallel_units", 1) if ps["type"] == "assisted_assembly_station" else 1
        slots.append((ps, max(1, int(n))))
    nslots = len(slots)
    span = max(LX - 2 * margin, 1.0)
    xs = [round(margin + (i * span / (nslots - 1) if nslots > 1 else span / 2), 2)
          for i in range(nslots)]

    stations, slot_ids, info_panels, safety_zones = [], [], [], []
    for i, (ps, n) in enumerate(slots):
        x = xs[i]
        t = ps["type"]
        dx, dy, dz = DIMS[t]
        here = []
        for j in range(n):
            iid = ps["id"] + (chr(ord("A") + j) if n > 1 else "")
            y = round(line_y + (j - (n - 1) / 2.0) * par_offset, 2) if n > 1 else line_y
            short = SHORT[t]
            suffix = ("_" + chr(ord("A") + j)) if n > 1 else ""
            info_name = "INFO_%s_Panel%s" % (short, suffix)
            trig_name = "TRIGGER_Info_%s%s" % (short, suffix)
            st = {
                "id": iid, "type": t, "name": "STATION_%s_%s" % (iid, short),
                "position": [x, y, 0.0], "rotation_deg": [0, 0, 0],
                "dimensions_m": {"x": dx, "y": dy, "z": dz},
                "prefab": PREFAB[t], "info_panel": info_name, "trigger": trig_name,
                "reasoning_key": REASON[t],
            }
            if n > 1:
                st["parallel_group"] = ps["id"]
            stations.append(st)
            here.append(iid)
            # info panel toward the walkway
            ipy = round(min(y + 2.6, walkway_y - 1.5), 2)
            info_panels.append({"id": "IP_%s" % iid, "station": iid, "name": info_name,
                                "position": [x, ipy, 1.6]})
            if t == "robot_handling_cell":
                safety_zones.append({
                    "id": "F_%s" % iid, "name": "STATION_%s_RobotCell_Fence" % iid,
                    "station": iid, "type": "robot_cell_fence",
                    "area_min": [round(x - 1.4, 2), round(y - 1.4, 2), 0.0],
                    "area_max": [round(x + 1.4, 2), round(y + 1.4, 2), 0.0],
                    "height_m": 2.0,
                    "access_gate": {"side": "+Y", "center": [x, round(y + 1.4, 2), 0.0],
                                    "width_m": 1.0, "interlocked": True}})
        slot_ids.append(here)

    # conveyors: fan-out / fan-in between consecutive slots
    conveyors, ci = [], 1
    pos = {s["id"]: s["position"] for s in stations}
    for i in range(nslots - 1):
        for a in slot_ids[i]:
            for b in slot_ids[i + 1]:
                ax, ay, _ = pos[a]
                bx, by, _ = pos[b]
                conveyors.append({
                    "id": "C%02d" % ci, "name": "CONVEYOR_%s_%s" % (a, b),
                    "from": a, "to": b,
                    "start": [round(ax + 1.0, 2), ay, 0.4], "end": [round(bx - 1.0, 2), by, 0.4],
                    "width_m": 0.6, "height_m": 0.4, "belt_speed_mps": 0.15, "kinematic": True})
                ci += 1

    # avatar walkway: one inspection waypoint per slot along the aisle
    wps = [{"id": "W00", "role": "entry", "position": [round(margin - 1.0, 2), walkway_y, 0.0]}]
    for i, (ps, n) in enumerate(slots):
        wps.append({"id": "W%02d" % (i + 1), "role": "inspect", "station": slot_ids[i][0],
                    "position": [xs[i], walkway_y, 0.0]})
    wps.append({"id": "W99", "role": "exit", "position": [round(LX - margin + 1.0, 2), walkway_y, 0.0]})

    fd = {
        "schema_version": "0.3",
        "scene": {
            "name": plan.get("line_name", "Line").replace(" ", "_"),
            "description": "Positioned station instances generated from the planned line.",
            "product": plan.get("product", ""),
            "generator": "planning/plan_to_factory_description.py",
            "coordinate_system": "Z-up (Blender). Export converts to Y-up for Unity.",
            "flow_direction": "+X",
        },
        "unit_system": {"units": "meters", "scale": 1.0},
        "factory_floor": {"size_m": {"x": LX, "y": WY}, "origin": [0.0, 0.0, 0.0],
                          "line_y_m": line_y, "walkway_y_m": walkway_y},
        "stations": stations,
        "conveyors": conveyors,
        "avatar_walkway": {"name": "PATH_AvatarWalkway", "width_m": 1.6, "waypoints": wps},
        "info_panels": info_panels,
        "safety_zones": safety_zones,
        "export_settings": {"mode": "per_station_prefab", "up_axis": "Y",
                            "note": "Blender exports individual station GLBs; Unity assembles the line."},
    }
    return fd


def main():
    plan_path = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(_REQ, "production_line_plan.json")
    out_path = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(_REQ, "factory_description.json")
    plan = load_json(plan_path)
    fd = build(plan)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(fd, fh, indent=2)
    par = [s for s in fd["stations"] if s.get("parallel_group")]
    print("factory_description: %d station instances (%d parallel), %d conveyors, %d waypoints"
          % (len(fd["stations"]), len(par), len(fd["conveyors"]), len(fd["avatar_walkway"]["waypoints"])))
    print("wrote", out_path)


if __name__ == "__main__":
    main()
