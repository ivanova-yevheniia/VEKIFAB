"""
generate_unity_layout.py — build the WP B -> WP D handoff file.

Input:  requirements/factory_description.json
        reasoning/reasoning_summary.json  (optional, for UI keys)
        exports/glb/                       (to flag which prefabs already exist)
Output: unity_handoff/unity_factory_layout.json

Describes station prefab filenames, placements, triggers, reasoning keys, conveyor
connections, the avatar walkway and the physics expectations Unity applies by
object-name prefix. Blender exports individual station prefabs only — Unity
assembles the full line. Standard library only. Deterministic. No Blender.
"""

import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_B_ROOT = os.path.dirname(_HERE)


def load_json(p):
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _dist(a, b):
    return round(sum((a[i] - b[i]) ** 2 for i in range(2)) ** 0.5, 3)


def main():
    fd = load_json(os.path.join(_B_ROOT, "requirements", "factory_description.json"))
    reasoning_path = os.path.join(_B_ROOT, "reasoning", "reasoning_summary.json")
    reasoning = load_json(reasoning_path) if os.path.isfile(reasoning_path) else {"stations": {}}
    glb_dir = os.path.join(_B_ROOT, "exports", "glb")
    have = set(os.listdir(glb_dir)) if os.path.isdir(glb_dir) else set()

    # unique prefabs to generate in Blender (one per station type)
    prefabs, seen = [], set()
    for st in fd["stations"]:
        pf = st.get("prefab")
        if pf and pf not in seen:
            seen.add(pf)
            prefabs.append({"type": st["type"], "prefab_glb": pf,
                            "exists_in_exports": pf in have})

    placements = []
    for st in fd["stations"]:
        rk = st.get("reasoning_key")
        placements.append({
            "station_id": st["id"], "type": st["type"], "prefab_glb": st.get("prefab"),
            "position_m": st["position"], "rotation_deg": st.get("rotation_deg", [0, 0, 0]),
            "scale": 1.0,
            "trigger": st.get("trigger"), "info_panel": st.get("info_panel"),
            "reasoning_key": rk, "reasoning_available": rk in reasoning.get("stations", {}),
            "parallel_group": st.get("parallel_group"),
        })

    wps = fd["avatar_walkway"]["waypoints"]
    route = round(sum(_dist(wps[i]["position"], wps[i + 1]["position"]) for i in range(len(wps) - 1)), 3)

    layout = {
        "schema_version": "1.0",
        "handoff": "WP B (Blender station prefabs) -> WP D (Unity assembly + avatar)",
        "project": "VEKIFAB — AI Factory Planner",
        "product": fd["scene"].get("product", ""),
        "units": "meters", "up_axis": "Y (glTF)",
        "factory_floor_m": fd["factory_floor"]["size_m"],
        "assembly_note": "Blender exports individual station GLBs. Unity instantiates one prefab "
                         "per placement below and assembles the line; Blender does NOT export a full scene.",
        "prefabs_to_generate": prefabs,
        "station_placements": placements,
        "conveyors": [{"id": c["id"], "name": c["name"], "from": c["from"], "to": c["to"],
                       "start_m": c["start"], "end_m": c["end"], "width_m": c.get("width_m", 0.6),
                       "belt_speed_mps": c.get("belt_speed_mps", 0.15)} for c in fd["conveyors"]],
        "avatar_walkway": {"name": fd["avatar_walkway"]["name"],
                           "width_m": fd["avatar_walkway"]["width_m"],
                           "waypoints_m": [w["position"] for w in wps],
                           "route_length_m": route},
        "info_panels": [{"id": ip["id"], "station": ip["station"], "name": ip["name"],
                         "position_m": ip["position"]} for ip in fd["info_panels"]],
        "safety_zones": fd.get("safety_zones", []),
        "physics_expectations": {
            "by_name_prefix": {
                "COLLIDER_": "Static collider (convex box); no Rigidbody",
                "PHYS_": "Rigidbody (dynamic); use kinematic if tagged kinematic",
                "TRIGGER_": "Collider with isTrigger = true; usually no renderer",
                "INFO_": "UI data source (bind to reasoning_summary.json)",
                "CONVEYOR_": "Kinematic belt; moves product at belt_speed_mps",
                "STATION_": "Structural / static station geometry"
            },
            "custom_property_source": "glTF extras (unity_tag, collider, rigidbody, mass, kinematic, is_trigger, station_id)"
        },
        "reasoning_source": "reasoning/reasoning_summary.json",
    }
    out = os.path.join(_HERE, "unity_factory_layout.json")
    json.dump(layout, open(out, "w", encoding="utf-8"), indent=2)
    print("unity_factory_layout.json: %d placements, %d prefabs (%d already exported), route %.1f m"
          % (len(placements), len(prefabs), sum(1 for p in prefabs if p["exists_in_exports"]), route))


if __name__ == "__main__":
    main()
