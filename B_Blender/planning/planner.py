"""
planner.py — VEKIFAB AI Factory Planner.

Reads a customer_requirements.json and decides *which stations the production line
needs* — reasoning about daily production, automation level, floor area, workers,
quality requirements and budget. It is the first component that makes engineering
decisions instead of following a fixed sequence.

Outputs:
  production_line_plan.json  — the generated line (pipeline-compatible)
  planner_decisions.md       — a human-readable explanation of every decision

Standard library only. Deterministic. No Blender.

Usage:
  python planner.py <customer_requirements.json> [output_dir]
  python planner.py            # batch: process every planning_examples/*/customer_requirements.json
"""

import os
import sys
import json
import math
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))


def load_json(p):
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _norm_automation(level):
    s = str(level or "semi").lower()
    if s.startswith("man"):
        return "manual"
    if s.startswith("full") or "fully" in s:
        return "full"
    return "semi"


class Planner:
    def __init__(self, rules=None):
        self.rules = rules or load_json(os.path.join(_HERE, "planning_rules.json"))
        self.cat = self.rules["station_catalog"]
        self.auto_rank = self.rules["automation_levels"]
        self.budget_rank = self.rules["budget_tiers"]

    # -- requirement getters (robust to partial inputs) --------------------
    @staticmethod
    def _g(req, path, default=None):
        cur = req
        for k in path.split("."):
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                return default
        return cur

    def _read(self, req):
        shift = self.rules["shift"]
        r = {}
        r["name"] = self._g(req, "customer.name", "Customer")
        r["product"] = self._g(req, "product.name", "Product")
        r["daily_output"] = int(self._g(req, "daily_output.target_units_per_day", 0) or 0)
        r["shift_hours"] = float(self._g(req, "daily_output.shift_hours", shift["default_hours"]))
        r["shifts"] = float(self._g(req, "daily_output.shifts_per_day", shift["default_shifts"]))
        r["cycle_time_s"] = float(self._g(req, "product.target_cycle_time_s",
                                          self._g(req, "daily_output.target_cycle_time_s",
                                                  shift["default_cycle_time_s"])))
        r["automation"] = _norm_automation(self._g(req, "automation_level.level", "semi"))
        lx = float(self._g(req, "available_area_m.length_x", 0) or 0)
        wy = float(self._g(req, "available_area_m.width_y", 0) or 0)
        r["length_x"] = lx
        r["width_y"] = wy
        r["area_m2"] = round(lx * wy, 1)
        r["workers"] = int(self._g(req, "workers.total", 0) or 0)
        methods = self._g(req, "quality_control.methods", []) or []
        r["quality_methods"] = [str(m).lower() for m in methods]
        r["regulated"] = bool(self._g(req, "quality_control.regulated", False))
        r["budget"] = str(self._g(req, "constraints.budget",
                                  self._g(req, "budget", "medium")) or "medium").lower()
        return r

    def _budget_ok(self, budget, need):
        return self.budget_rank.get(budget, 1) >= self.budget_rank.get(need, 0)

    def _quality_hit(self, methods, keywords):
        return any(any(k in m for m in methods) for k in keywords)

    # -- the decision logic ------------------------------------------------
    def plan(self, req):
        r = self._read(req)
        rules = self.rules["rules"]
        decisions = []
        shift_seconds = r["shift_hours"] * r["shifts"] * 3600.0

        def dec(name, included, rule, rationale, value=None):
            decisions.append({"decision": name, "included": included, "value": value,
                              "rule": rule, "rationale": rationale})

        # --- automation tier ---
        tier = r["automation"]
        wpr = (r["daily_output"] / r["workers"]) if r["workers"] else 0
        dec("Automation tier", True, "automation_level.level (normalized)",
            "Declared automation is '%s'; %d units/worker/day → tier drives which "
            "automated stations are viable." % (tier, round(wpr)), value=tier)

        # --- parallel assembly (throughput) ---
        acycle = self.cat["assisted_assembly_station"]["cycle_time_s"]
        cap = math.floor(shift_seconds / acycle) if acycle else r["daily_output"]
        need = max(1, math.ceil(r["daily_output"] / cap)) if cap else 1
        par_budget = rules["parallel_assembly"]["requires_budget_at_least"]
        if need >= rules["parallel_assembly"]["min_units_to_flag"] and self._budget_ok(r["budget"], par_budget):
            assembly_units = need
            dec("Parallel assembly", True, "ceil(daily_output / single-station capacity)",
                "Capacity per assembly ≈ %d/shift but %d/day required → %d parallel "
                "assembly stations to hold takt." % (cap, r["daily_output"], need),
                value=need)
        elif need >= 2:
            assembly_units = 1
            dec("Parallel assembly", False, "needs budget ≥ %s" % par_budget,
                "Throughput wants %d assembly stations, but budget '%s' blocks it → "
                "single station (throughput risk / add a second shift)." % (need, r["budget"]),
                value=1)
        else:
            assembly_units = 1
            dec("Parallel assembly", False, "single station meets takt",
                "One assembly station (cap ≈ %d/shift) covers %d/day." % (cap, r["daily_output"]),
                value=1)

        # --- robot cell ---
        rc = rules["robot_cell"]
        want_robot = (self.auto_rank[tier] >= self.auto_rank[rc["include_if_automation_at_least"]]
                      or r["daily_output"] >= rc["include_if_daily_output_at_least"])
        can_robot = self._budget_ok(r["budget"], rc["requires_budget_at_least"]) \
            and r["area_m2"] >= rc["requires_area_m2_at_least"]
        robot = want_robot and can_robot
        if robot:
            dec("Robot handling cell", True,
                "automation ≥ full OR daily_output ≥ %d; budget ≥ %s; area ≥ %d m²"
                % (rc["include_if_daily_output_at_least"], rc["requires_budget_at_least"], rc["requires_area_m2_at_least"]),
                "High automation / throughput justifies a robot; budget and %g m² floor allow it."
                % r["area_m2"])
        elif want_robot and not can_robot:
            dec("Robot handling cell", False, "blocked by budget/area gate",
                "Automation/throughput wants a robot, but budget '%s' or area %g m² "
                "is insufficient → manual/assisted handling instead." % (r["budget"], r["area_m2"]))
        else:
            dec("Robot handling cell", False, "low automation & throughput",
                "Automation '%s' and %d/day do not justify a robot → no robot cell."
                % (tier, r["daily_output"]))

        # --- vision inspection ---
        vi = rules["vision_inspection"]
        vision = (self._quality_hit(r["quality_methods"], vi["quality_keywords"])
                  or (vi["include_if_regulated"] and r["regulated"])) \
            and self._budget_ok(r["budget"], vi["requires_budget_at_least"])
        dec("Vision inspection", vision,
            "quality mentions %s OR regulated; budget ≥ %s" % (vi["quality_keywords"], vi["requires_budget_at_least"]),
            ("Quality/regulatory needs objective optical inspection → include vision." if vision
             else "No high/optical quality requirement and not regulated → skip vision."))

        # --- functional test ---
        ft = rules["functional_test"]
        test = (self._quality_hit(r["quality_methods"], ft["quality_keywords"])
                or (ft["include_if_regulated"] and r["regulated"])) \
            and self._budget_ok(r["budget"], ft["requires_budget_at_least"])
        dec("Functional test", test,
            "quality mentions %s OR regulated; budget ≥ %s" % (ft["quality_keywords"], ft["requires_budget_at_least"]),
            ("Functional/regulated requirement → per-unit end-of-line test." if test
             else "No functional-test / regulatory requirement → skip functional test."))

        # --- compact layout ---
        compact = 0 < r["area_m2"] <= rules["compact_layout"]["max_area_m2"]
        dec("Compact layout", compact, "area ≤ %d m²" % rules["compact_layout"]["max_area_m2"],
            ("Small %g m² floor → compact spacing." % r["area_m2"] if compact
             else "Ample %g m² floor → standard spacing." % r["area_m2"]))

        # --- assemble the ordered station sequence ---
        seq = ["loading_station", "assisted_assembly_station"]
        if robot:
            seq.append("robot_handling_cell")
        if vision:
            seq.append("vision_inspection_station")
        if test:
            seq.append("functional_test_station")
        seq += ["packaging_station", "finished_goods_storage"]

        plan = self._build_plan(r, seq, assembly_units, compact, shift_seconds)
        # area feasibility note
        used = sum(self.cat[t]["area_m2"] * (assembly_units if t == "assisted_assembly_station" else 1)
                   for t in seq)
        dec("Floor-area feasibility", used <= r["area_m2"] if r["area_m2"] else True,
            "sum(station area) ≤ available area",
            "Stations need ≈ %.0f m²; available %g m²." % (used, r["area_m2"]),
            value=round(used, 1))
        plan["planner"]["stations_area_m2"] = round(used, 1)
        return plan, decisions, r

    def _build_plan(self, r, seq, assembly_units, compact, shift_seconds):
        layout = self.rules["layout"]
        spacing = layout["compact_spacing_m"] if compact else layout["spacing_m"]
        x = layout["origin_x_m"]
        stations = []
        for i, t in enumerate(seq, 1):
            c = self.cat[t]
            sid = "S%02d" % i
            entry = {
                "id": sid, "type": t, "name": c["name"], "purpose": c["purpose"],
                "input": c["input"], "output": c["output"],
                "cycle_role": "%d s nominal" % c["cycle_time_s"],
                "required_equipment": c["required_equipment"],
                "info_panel_text": c["info_panel_text"],
                "position_m": [round(x, 2), layout["y_center_m"], 0.0],
            }
            if t == "assisted_assembly_station" and assembly_units > 1:
                entry["parallel_units"] = assembly_units
            stations.append(entry)
            x += spacing
        conveyors = [{"id": "C%02d" % i, "from": stations[i - 1]["id"], "to": stations[i]["id"]}
                     for i in range(1, len(stations))]
        throughput_hr = round(r["daily_output"] / (r["shift_hours"] * r["shifts"]), 1) \
            if r["shift_hours"] else 0
        return {
            "schema_version": "1.0",
            "line_name": "%s Line" % r["product"],
            "product": r["product"],
            "generated_by": "planning/planner.py",
            "throughput_target_per_hour": throughput_hr,
            "target_cycle_time_s": r["cycle_time_s"],
            "flow_direction": layout["flow_direction"],
            "planner": {
                "automation_tier": r["automation"],
                "daily_output": r["daily_output"],
                "available_area_m": {"length_x": r["length_x"], "width_y": r["width_y"]},
                "available_area_m2": r["area_m2"],
                "workers": r["workers"],
                "budget": r["budget"],
                "regulated": r["regulated"],
                "layout": "compact" if compact else "standard",
                "assembly_units": assembly_units,
                "station_count": len(stations),
                "decisions_ref": "planner_decisions.md",
            },
            "stations": stations,
            "conveyors": conveyors,
        }


def decisions_md(plan, decisions, r):
    L = []
    L.append("# Planner Decisions — %s" % plan["line_name"])
    L.append("")
    L.append("*Generated by `planning/planner.py` from customer requirements.*")
    L.append("")
    L.append("## Inputs")
    L.append("")
    L.append("| Input | Value |")
    L.append("|-------|-------|")
    for k, v in [("Product", r["product"]), ("Daily output", "%d/day" % r["daily_output"]),
                 ("Automation", r["automation"]), ("Floor area", "%g m²" % r["area_m2"]),
                 ("Workers", r["workers"]), ("Quality", ", ".join(r["quality_methods"]) or "basic"),
                 ("Regulated", r["regulated"]), ("Budget", r["budget"])]:
        L.append("| %s | %s |" % (k, v))
    L.append("")
    L.append("## Decisions")
    L.append("")
    L.append("| Decision | Result | Rule | Rationale |")
    L.append("|----------|--------|------|-----------|")
    for d in decisions:
        res = d["value"] if d["value"] is not None else ("YES" if d["included"] else "NO")
        L.append("| %s | %s | %s | %s |" % (d["decision"], res, d["rule"], d["rationale"]))
    L.append("")
    L.append("## Resulting line (%d stations, %s layout)" %
             (plan["planner"]["station_count"], plan["planner"]["layout"]))
    L.append("")
    for s in plan["stations"]:
        extra = " ×%d (parallel)" % s["parallel_units"] if s.get("parallel_units") else ""
        L.append("- **%s** — %s%s" % (s["id"], s["name"], extra))
    L.append("")
    L.append("Flow: " + " → ".join(s["id"] for s in plan["stations"]) +
             "  (%s)" % plan["flow_direction"])
    L.append("")
    return "\n".join(L)


def run_one(req_path, out_dir=None):
    out_dir = out_dir or os.path.dirname(req_path)
    req = load_json(req_path)
    plan, decisions, r = Planner().plan(req)
    with open(os.path.join(out_dir, "production_line_plan.json"), "w", encoding="utf-8") as fh:
        json.dump(plan, fh, indent=2)
    with open(os.path.join(out_dir, "planner_decisions.md"), "w", encoding="utf-8") as fh:
        fh.write(decisions_md(plan, decisions, r))
    return plan


def main():
    if len(sys.argv) >= 2:
        plan = run_one(sys.argv[1], sys.argv[2] if len(sys.argv) >= 3 else None)
        print("planned %d stations: %s" %
              (plan["planner"]["station_count"], " -> ".join(s["id"] for s in plan["stations"])))
        return
    examples = sorted(glob.glob(os.path.join(_HERE, "planning_examples", "*", "customer_requirements.json")))
    if not examples:
        print("no examples found; pass a requirements file as an argument")
        return
    for ex in examples:
        plan = run_one(ex)
        name = os.path.basename(os.path.dirname(ex))
        types = [s["type"].replace("_station", "").replace("_", "") for s in plan["stations"]]
        au = plan["planner"]
        print("%-26s %d stations [%s] tier=%s layout=%s assembly=x%d" %
              (name, au["station_count"], ", ".join(s["id"] for s in plan["stations"]),
               au["automation_tier"], au["layout"], au["assembly_units"]))


if __name__ == "__main__":
    main()
