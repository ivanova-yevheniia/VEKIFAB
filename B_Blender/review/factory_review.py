"""
factory_review.py — VEKIFAB Factory Review (demo layer).

Validates the composed factory against review_rules.json and writes a scored
report (0-100) to factory_review_report.md and factory_review_report.json.

Standard library only. Deterministic. No Blender required.
"""

import os
import sys
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_B_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_B_ROOT, "composer"))

from factory_composer import FactoryComposer  # noqa: E402


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _station_aabb_xy(meta):
    cx, cy, _ = meta["world_position_m"]
    ex, ey = meta["envelope_m"]["x"], meta["envelope_m"]["y"]
    return (cx - ex / 2.0, cy - ey / 2.0, cx + ex / 2.0, cy + ey / 2.0)


def _overlap_xy(a, b, gap=0.0):
    return not (a[2] <= b[0] + gap or b[2] <= a[0] + gap or
                a[3] <= b[1] + gap or b[3] <= a[1] + gap)


class FactoryReview:
    def __init__(self):
        self.fc = FactoryComposer()
        self.rules = load_json(os.path.join(_HERE, "review_rules.json"))
        self.checks = []
        self.warnings = []
        self.recommendations = []

    def _assets_by_station(self):
        out = {}
        for s in self.fc.stations:
            out[s["meta"]["id"]] = [i["asset_id"] for i in s["composition"]["instances"]]
        return out

    # -- individual checks return (ratio in 0..1, detail str) ---------------
    def c_info_panels_present(self):
        by = self._assets_by_station()
        ok = [sid for sid, a in by.items() if "information_panel" in a]
        return len(ok) / len(by), "%d/%d stations have an info panel" % (len(ok), len(by))

    def c_safety_asset_present(self):
        by = self._assets_by_station()
        safe = set(self.rules["safety_assets"])
        ok = [sid for sid, a in by.items() if safe.intersection(a)]
        return len(ok) / len(by), "%d/%d stations have a safety asset" % (len(ok), len(by))

    def c_material_flow_connected(self):
        edges = {}
        for c in self.fc.conveyors():
            edges.setdefault(c["from"], []).append(c["to"])
        start, end = self.rules["flow_start"], self.rules["flow_end"]
        seen, stack = set(), [start]
        while stack:
            n = stack.pop()
            if n == end:
                return 1.0, "flow path %s -> %s exists" % (start, end)
            for m in edges.get(n, []):
                if m not in seen:
                    seen.add(m); stack.append(m)
        return 0.0, "no connected material flow from %s to %s" % (start, end)

    def c_conveyors_adjacent(self):
        order = self.rules["station_order"]
        idx = {s: i for i, s in enumerate(order)}
        required = {(order[i], order[i + 1]) for i in range(len(order) - 1)}
        present = set()
        for c in self.fc.conveyors():
            f, t = c["from"], c["to"]
            if f in idx and t in idx and idx[t] - idx[f] == 1:
                present.add((f, t))
        cov = len(present & required) / len(required)
        return cov, "%d/%d adjacent station pairs connected by a conveyor" % (
            len(present & required), len(required))

    def c_walkway_no_intersection(self):
        wp = self.fc.walkway().get("waypoints_m", [])
        if not wp:
            return 0.0, "no avatar walkway defined"
        gap = self.rules["walkway_min_clearance_m"]
        boxes = [_station_aabb_xy(s["meta"]) for s in self.fc.stations]
        hits = 0
        for p in wp:
            for (x0, y0, x1, y1) in boxes:
                if (x0 - gap) <= p[0] <= (x1 + gap) and (y0 - gap) <= p[1] <= (y1 + gap):
                    hits += 1
                    break
        if hits:
            return 0.0, "walkway intersects station footprints at %d waypoint(s)" % hits
        return 1.0, "walkway of %d waypoints clears all footprints" % len(wp)

    def c_emergency_stop_required(self):
        by = self._assets_by_station()
        req = self.rules["emergency_stop_required_stations"]
        ok = [sid for sid in req if "emergency_stop" in by.get(sid, [])]
        return len(ok) / len(req), "%d/%d required stations have an emergency stop" % (len(ok), len(req))

    def c_physics_objects_tagged(self):
        insts = [i for i in self.fc.all_instances()
                 if i.get("physics_role") in ("dynamic", "kinematic")]
        if not insts:
            return 1.0, "no dynamic/kinematic objects to tag"
        tagged = [i for i in insts if i.get("unity_tags")]
        return len(tagged) / len(insts), "%d/%d physics objects tagged" % (len(tagged), len(insts))

    def c_naming_conventions(self):
        allowed = tuple(self.rules["allowed_name_prefixes"])
        trig = set(self.rules["trigger_roles"])
        insts = self.fc.all_instances()
        bad = []
        for i in insts:
            name = i.get("name_prefix", "")
            if not name.startswith(allowed):
                bad.append(i["instance_id"])
                continue
            if i.get("physics_role") in trig and "Trigger" not in i.get("unity_tags", []):
                bad.append(i["instance_id"])
        ratio = 1.0 - len(bad) / len(insts) if insts else 1.0
        return ratio, "%d/%d instances follow naming/tag conventions" % (len(insts) - len(bad), len(insts))

    def c_no_duplicate_instance_ids(self):
        dup = self.fc.duplicate_instance_ids()
        return (0.0 if dup else 1.0), ("duplicates: %s" % ", ".join(dup) if dup else "no duplicate instance ids")

    def c_no_missing_asset_refs(self):
        miss = self.fc.missing_asset_refs()
        return (0.0 if miss else 1.0), ("missing: %s" % ", ".join(miss) if miss else "all asset references resolve")

    def c_no_overlapping_footprints(self):
        metas = [s["meta"] for s in self.fc.stations]
        boxes = [(_station_aabb_xy(m), m["id"]) for m in metas]
        overlaps = []
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if _overlap_xy(boxes[i][0], boxes[j][0]):
                    overlaps.append("%s&%s" % (boxes[i][1], boxes[j][1]))
        return (0.0 if overlaps else 1.0), ("overlaps: %s" % ", ".join(overlaps)
                                            if overlaps else "no overlapping footprints")

    # -- run ---------------------------------------------------------------
    def run(self):
        fns = {
            "info_panels_present": self.c_info_panels_present,
            "safety_asset_present": self.c_safety_asset_present,
            "material_flow_connected": self.c_material_flow_connected,
            "conveyors_adjacent": self.c_conveyors_adjacent,
            "walkway_no_intersection": self.c_walkway_no_intersection,
            "emergency_stop_required": self.c_emergency_stop_required,
            "physics_objects_tagged": self.c_physics_objects_tagged,
            "naming_conventions": self.c_naming_conventions,
            "no_duplicate_instance_ids": self.c_no_duplicate_instance_ids,
            "no_missing_asset_refs": self.c_no_missing_asset_refs,
            "no_overlapping_footprints": self.c_no_overlapping_footprints,
        }
        score = 0.0
        for spec in self.rules["checks"]:
            cid = spec["id"]; weight = spec["weight"]
            ratio, detail = fns[cid]()
            earned = round(weight * ratio, 2)
            score += earned
            status = "pass" if ratio >= 0.999 else ("warn" if ratio > 0 else "fail")
            self.checks.append({
                "id": cid, "description": spec["description"], "status": status,
                "weight": weight, "earned": earned, "detail": detail,
            })
            if status == "warn":
                self.warnings.append("%s — %s" % (cid, detail))
            if status != "pass":
                self.recommendations.append(self._recommend(cid, detail))
        self.score = int(round(score))
        return self.score

    @staticmethod
    def _recommend(cid, detail):
        tips = {
            "info_panels_present": "Add an information_panel instance to every station.",
            "safety_asset_present": "Add a safety asset (emergency_stop / stack_light / safety_fence).",
            "material_flow_connected": "Ensure conveyors chain S01->...->S07 without gaps.",
            "conveyors_adjacent": "Add conveyor connections for every adjacent station pair.",
            "walkway_no_intersection": "Move the walkway clear of station footprints.",
            "emergency_stop_required": "Add an emergency_stop to each required (manned) station.",
            "physics_objects_tagged": "Tag every dynamic/kinematic instance with Unity tags.",
            "naming_conventions": "Rename instances to the STATION_/COLLIDER_/CONVEYOR_/PHYS_/TRIGGER_/INFO_ scheme.",
            "no_duplicate_instance_ids": "Make every instance_id unique.",
            "no_missing_asset_refs": "Reference only assets present in asset_registry.json.",
            "no_overlapping_footprints": "Re-space stations so footprints do not overlap.",
        }
        return "%s: %s (%s)" % (cid, tips.get(cid, "review this check"), detail)

    # -- output ------------------------------------------------------------
    def write_reports(self):
        rep = {
            "schema_version": "1.0",
            "project": self.fc.factory["project"]["name"],
            "score": self.score,
            "score_max": self.rules["score_max"],
            "verdict": self._verdict(),
            "checks": self.checks,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
        }
        with open(os.path.join(_HERE, "factory_review_report.json"), "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=2)
        with open(os.path.join(_HERE, "factory_review_report.md"), "w", encoding="utf-8") as fh:
            fh.write(self._markdown(rep))
        return rep

    def _verdict(self):
        if self.score >= 90:
            return "PASS — production-ready composition"
        if self.score >= 75:
            return "PASS with minor issues"
        if self.score >= 50:
            return "NEEDS WORK"
        return "FAIL"

    def _markdown(self, rep):
        lines = []
        lines.append("# Factory Review Report")
        lines.append("")
        lines.append("**Project:** %s  " % rep["project"])
        lines.append("**Score:** %d / %d  " % (rep["score"], rep["score_max"]))
        lines.append("**Verdict:** %s" % rep["verdict"])
        lines.append("")
        lines.append("## Checks")
        lines.append("")
        lines.append("| Check | Status | Score | Detail |")
        lines.append("|-------|--------|-------|--------|")
        icon = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}
        for c in rep["checks"]:
            lines.append("| %s | %s | %.2f/%d | %s |" % (
                c["id"], icon[c["status"]], c["earned"], c["weight"], c["detail"]))
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        if rep["warnings"]:
            for w in rep["warnings"]:
                lines.append("- %s" % w)
        else:
            lines.append("- none")
        lines.append("")
        lines.append("## Recommended improvements")
        lines.append("")
        if rep["recommendations"]:
            for r in rep["recommendations"]:
                lines.append("- %s" % r)
        else:
            lines.append("- none — all checks passed")
        lines.append("")
        return "\n".join(lines)


def main():
    rv = FactoryReview()
    score = rv.run()
    rep = rv.write_reports()
    print("Factory Review: score %d/100 — %s" % (score, rep["verdict"]))
    print("  checks:", sum(1 for c in rv.checks if c["status"] == "pass"), "pass /",
          sum(1 for c in rv.checks if c["status"] == "warn"), "warn /",
          sum(1 for c in rv.checks if c["status"] == "fail"), "fail")
    print("  warnings:", len(rv.warnings))
    print("  wrote factory_review_report.md / .json")


if __name__ == "__main__":
    main()
