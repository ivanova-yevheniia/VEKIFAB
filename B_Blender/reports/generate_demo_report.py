"""
generate_demo_report.py — VEKIFAB demo report (demo layer).

Writes demo_report.md and demo_report.json from factory_metrics.collect().
Standard library only; deterministic; no Blender required.
"""

import os
import json

import factory_metrics

_HERE = os.path.dirname(os.path.abspath(__file__))


def _markdown(m):
    L = []
    L.append("# VEKIFAB — AI Factory Planner · Demo Report")
    L.append("")
    L.append("**Project:** %s  " % m["project_name"])
    L.append("**Use case:** %s  " % m["use_case"])
    L.append("**Product:** %s  " % m["product"])
    L.append("**Factory area:** %s m² (%s × %s m)" % (
        m["factory_area_m2"], m["factory_floor_m"].get("x"), m["factory_floor_m"].get("y")))
    if m["review_score"] is not None:
        L.append("**Review score:** %s / 100" % m["review_score"])
    L.append("")
    L.append("## Key metrics")
    L.append("")
    L.append("| Metric | Value |")
    L.append("|--------|-------|")
    rows = [
        ("Stations", m["stations"]),
        ("Asset instances", m["asset_instances"]),
        ("Conveyors", m["conveyors"]),
        ("Info panels", m["info_panels"]),
        ("Physics objects", m["physics_objects"]),
        ("Collider candidates", m["collider_candidates"]),
        ("Trigger zones", m["trigger_zones"]),
        ("Estimated conveyor length", "%s m" % m["conveyor_length_m"]),
        ("Avatar route length", "%s m" % m["avatar_route_length_m"]),
        ("Exported files", m["exported_file_count"]),
    ]
    for k, v in rows:
        L.append("| %s | %s |" % (k, v))
    L.append("")
    L.append("## Asset coverage by category")
    L.append("")
    L.append("| Category | Instances |")
    L.append("|----------|-----------|")
    for cat, n in m["asset_coverage_by_category"].items():
        L.append("| %s | %d |" % (cat, n))
    L.append("")
    L.append("## Generated / exported files")
    L.append("")
    any_files = False
    for sub in ("blend", "glb", "screenshots"):
        files = m["exported_files"].get(sub, [])
        if files:
            any_files = True
            L.append("**exports/%s/**" % sub)
            for f in files:
                L.append("- `%s`" % f)
    if not any_files:
        L.append("- none yet (run the procedural builder to export station geometry)")
    L.append("")
    L.append("## The AI pipeline")
    L.append("")
    L.append(" → ".join(m["pipeline"]))
    L.append("")
    L.append("1. **Customer requirements** — the client's production needs "
             "(`requirements/customer_requirements.json`).")
    L.append("2. **Process plan** — the ordered line of stations "
             "(`requirements/production_line_plan.json`, `factory_description.json`).")
    L.append("3. **Asset composition** — each station composed as a bill of reusable "
             "industrial assets (`composer/`, `assets/`).")
    L.append("4. **Procedural builder** — the generic JSON-driven renderer "
             "(`procedural_builder/`) turns specs into geometry.")
    L.append("5. **Blender** — exports `.blend` / `.glb` with Unity-ready colliders, "
             "triggers and tags.")
    L.append("6. **Unity avatar walkthrough** — an avatar walks the line and inspects "
             "each station via info-panel triggers.")
    L.append("")
    return "\n".join(L)


def main():
    m = factory_metrics.collect()
    with open(os.path.join(_HERE, "demo_report.json"), "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=2)
    with open(os.path.join(_HERE, "demo_report.md"), "w", encoding="utf-8") as fh:
        fh.write(_markdown(m))
    print("Demo report written: demo_report.md / demo_report.json")
    print("  stations=%d instances=%d conveyors=%d info=%d" % (
        m["stations"], m["asset_instances"], m["conveyors"], m["info_panels"]))
    print("  physics=%d colliders=%d triggers=%d" % (
        m["physics_objects"], m["collider_candidates"], m["trigger_zones"]))
    print("  conveyor=%.2fm avatar route=%.2fm exported files=%d" % (
        m["conveyor_length_m"], m["avatar_route_length_m"], m["exported_file_count"]))
    return m


if __name__ == "__main__":
    main()
