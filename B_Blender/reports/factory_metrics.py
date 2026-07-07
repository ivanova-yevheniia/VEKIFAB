"""
factory_metrics.py — VEKIFAB demo metrics (demo layer).

Collects deterministic, Blender-free metrics about the composed factory for the
demo report. Reuses the Factory Composer for resolved instances and topology.
Standard library only.
"""

import os
import sys
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_B_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_B_ROOT, "composer"))

from factory_composer import FactoryComposer  # noqa: E402


def list_exports():
    """Return existing exported files under exports/{blend,glb,screenshots}."""
    found = {}
    for sub in ("blend", "glb", "screenshots"):
        d = os.path.join(_B_ROOT, "exports", sub)
        files = []
        if os.path.isdir(d):
            files = sorted(f for f in os.listdir(d)
                           if not f.startswith(".") and os.path.isfile(os.path.join(d, f)))
        found[sub] = files
    return found


def review_score():
    """Return the last review score if a report exists, else None."""
    p = os.path.join(_B_ROOT, "review", "factory_review_report.json")
    if os.path.isfile(p):
        try:
            return json.load(open(p, encoding="utf-8")).get("score")
        except (ValueError, OSError):
            return None
    return None


def collect():
    fc = FactoryComposer()
    m = fc.metrics()
    floor = fc.factory.get("factory_floor", {}).get("size_m", {})
    area = round(float(floor.get("x", 0)) * float(floor.get("y", 0)), 2)
    proj = fc.factory["project"]
    exports = list_exports()
    export_count = sum(len(v) for v in exports.values())
    metrics = {
        "project_name": proj.get("name", ""),
        "use_case": proj.get("use_case", ""),
        "product": proj.get("product", ""),
        "factory_area_m2": area,
        "factory_floor_m": floor,
        "stations": m["stations"],
        "asset_instances": m["asset_instances"],
        "conveyors": m["conveyors"],
        "info_panels": m["info_panels"],
        "physics_objects": m["physics_objects"],
        "collider_candidates": m["collider_candidates"],
        "trigger_zones": m["trigger_zones"],
        "conveyor_length_m": m["conveyor_length_m"],
        "avatar_route_length_m": m["avatar_route_length_m"],
        "asset_coverage_by_category": m["category_coverage"],
        "exported_files": exports,
        "exported_file_count": export_count,
        "review_score": review_score(),
        "pipeline": [
            "customer requirements",
            "process plan",
            "asset composition",
            "procedural builder",
            "Blender",
            "Unity avatar walkthrough",
        ],
    }
    return metrics


if __name__ == "__main__":
    print(json.dumps(collect(), indent=2))
