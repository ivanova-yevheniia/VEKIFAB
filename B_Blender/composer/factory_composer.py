"""
factory_composer.py — VEKIFAB Factory Composer (demo layer).

Assembles the complete production line as a *bill of asset instances*. It loads
`factory_composition.json`, the per-station composition files and the industrial
`asset_registry.json`, and resolves every asset instance into world space.

It does NOT build Blender geometry — it only composes and exposes the data the
Review and Report layers consume. Python standard library only; deterministic.
"""

import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_B_ROOT = os.path.dirname(_HERE)


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


class FactoryComposer:
    def __init__(self, base_dir=None):
        self.base = base_dir or _B_ROOT
        self.composer_dir = os.path.join(self.base, "composer")
        self.factory = load_json(os.path.join(self.composer_dir, "factory_composition.json"))
        # Asset registry (ids + categories).
        reg_path = os.path.join(self.base, self.factory.get("asset_library",
                                                             "assets/asset_registry.json"))
        self.registry = load_json(reg_path)
        self.asset_ids = {a["id"] for a in self.registry["assets"]}
        self.asset_category = {a["id"]: a["category"] for a in self.registry["assets"]}
        # Per-station compositions (ordered as in factory_composition).
        self.stations = []
        for st in self.factory["stations"]:
            comp = load_json(os.path.join(self.composer_dir, st["composition_file"]))
            self.stations.append({"meta": st, "composition": comp})

    # -- resolution ---------------------------------------------------------
    def all_instances(self):
        """Every instance across all stations, with resolved world position."""
        out = []
        for s in self.stations:
            sid = s["meta"]["id"]
            ox, oy, oz = s["meta"]["world_position_m"]
            for inst in s["composition"]["instances"]:
                px, py, pz = inst["position"]
                item = dict(inst)
                item["station"] = sid
                item["world_position_m"] = [round(ox + px, 3), round(oy + py, 3), round(oz + pz, 3)]
                out.append(item)
        return out

    # -- topology accessors -------------------------------------------------
    def conveyors(self):
        return self.factory.get("conveyors", [])

    def walkway(self):
        return self.factory.get("avatar_walkway", {})

    def info_panels(self):
        return self.factory.get("info_panels", [])

    def safety_zones(self):
        return self.factory.get("safety_zones", [])

    def station_ids(self):
        return [s["meta"]["id"] for s in self.stations]

    def station_instances(self, sid):
        for s in self.stations:
            if s["meta"]["id"] == sid:
                return s["composition"]["instances"]
        return []

    # -- integrity ----------------------------------------------------------
    def duplicate_instance_ids(self):
        seen, dup = set(), []
        for inst in self.all_instances():
            iid = inst["instance_id"]
            if iid in seen:
                dup.append(iid)
            seen.add(iid)
        return sorted(set(dup))

    def missing_asset_refs(self):
        missing = []
        for inst in self.all_instances():
            if inst["asset_id"] not in self.asset_ids:
                missing.append(inst["asset_id"])
        return sorted(set(missing))

    # -- geometry-free measures --------------------------------------------
    @staticmethod
    def _dist(a, b):
        return sum((a[i] - b[i]) ** 2 for i in range(min(len(a), len(b)))) ** 0.5

    def conveyor_length_m(self):
        total = 0.0
        for c in self.conveyors():
            total += self._dist(c["start_m"], c["end_m"])
        return round(total, 3)

    def walkway_length_m(self):
        wps = self.walkway().get("waypoints_m", [])
        return round(sum(self._dist(wps[i], wps[i + 1]) for i in range(len(wps) - 1)), 3)

    def category_coverage(self):
        cov = {}
        for inst in self.all_instances():
            cat = self.asset_category.get(inst["asset_id"], "unknown")
            cov[cat] = cov.get(cat, 0) + 1
        return dict(sorted(cov.items()))

    def role_counts(self):
        counts = {}
        for inst in self.all_instances():
            r = inst.get("physics_role", "static")
            counts[r] = counts.get(r, 0) + 1
        return dict(sorted(counts.items()))

    def metrics(self):
        insts = self.all_instances()
        roles = self.role_counts()
        return {
            "stations": len(self.stations),
            "asset_instances": len(insts),
            "conveyors": len(self.conveyors()),
            "info_panels": len(self.info_panels()),
            "physics_objects": roles.get("dynamic", 0) + roles.get("kinematic", 0),
            "collider_candidates": roles.get("static", 0),
            "trigger_zones": roles.get("trigger", 0),
            "conveyor_length_m": self.conveyor_length_m(),
            "avatar_route_length_m": self.walkway_length_m(),
            "category_coverage": self.category_coverage(),
        }


def main():
    fc = FactoryComposer()
    m = fc.metrics()
    print("VEKIFAB Factory Composer")
    print("  project :", fc.factory["project"]["name"])
    print("  stations:", m["stations"])
    print("  instances:", m["asset_instances"])
    print("  conveyors:", m["conveyors"], "| info panels:", m["info_panels"])
    print("  physics objects:", m["physics_objects"],
          "| collider candidates:", m["collider_candidates"],
          "| triggers:", m["trigger_zones"])
    print("  conveyor length:", m["conveyor_length_m"], "m",
          "| avatar route:", m["avatar_route_length_m"], "m")
    dup = fc.duplicate_instance_ids()
    miss = fc.missing_asset_refs()
    print("  duplicate instance ids:", len(dup), "| missing asset refs:", len(miss))
    print("  category coverage:", m["category_coverage"])


if __name__ == "__main__":
    main()
