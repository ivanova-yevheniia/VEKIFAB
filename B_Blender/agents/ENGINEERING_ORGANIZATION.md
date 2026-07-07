# VEKIFAB — Virtual AI Engineering Organization (WP B)

## Purpose

The ten discipline reviewers under `agent_profiles/` are individual specialists.
This document defines the **organization** that coordinates them the way a real
industrial engineering house runs a design review before a machine ships: a
Chief Engineer plans the effort, specialists review their domain in sequence, an
Integration Engineer reconciles cross-discipline conflicts, Quality performs an
acceptance audit, and Management (CTO + Customer) makes the go/no-go call.

It is a **simulation of a real industrial design-review workflow** — plan →
engineer → integrate → inspect → accept — applied to a VEKIFAB station spec so
that any station (S01–S07) can be hardened to "Bosch-internal-demo / digital-twin"
quality by *editing only the two JSON spec files and rerunning the existing
procedural builder*. No agent invents geometry or new tooling.

---

## Organizational chart

```
                         ┌─────────────────────────┐
                         │   Customer Requirement   │  (VEKIFAB Planning output)
                         └────────────┬────────────┘
                                      │
                        ┌─────────────▼─────────────┐
                        │        MANAGEMENT          │
                        │  00 Chief Engineer  ───────┼──► plans & assigns
                        │  11 Integration Engineer   │
                        │  10 CTO Reviewer (gate)     │
                        │  13 Customer Representative │
                        └─────────────┬─────────────┘
             ┌───────────────┬────────┼─────────┬──────────────┐
             ▼               ▼        ▼         ▼              ▼
   ┌───────────────┐ ┌──────────────────────┐ ┌──────────┐ ┌──────────────┐
   │ 0. AI PLANNING│ │ 2. ENGINEERING DEPT   │ │3. DESIGN │ │ 4. QUALITY    │
   │  (upstream)   │ │ 01 Mechanical         │ │ 08 Indl. │ │ 12 QA Insp.   │
   │  requirements │ │ 02 Manufacturing      │ │ Designer │ │ 09 Operator   │
   │  + line plan  │ │ 03 Electrical         │ └──────────┘ └──────────────┘
   └───────────────┘ │ 04 Pneumatic          │
                     │ 05 Maintenance        │
                     │ 06 Safety             │
                     │ 07 Ergonomics         │
                     └──────────────────────┘

Flow: Plan → 01…08 specialists → 09 operator → 11 integration →
      12 QA punch list → fix loop → 10 CTO gate → 13 customer acceptance
```

> **File-prefix ≠ run-order.** The numeric prefix on a profile is a stable role
> ID. The execution sequence is defined in `orchestrator.md` (e.g. role `11`
> Integration runs *before* role `10` CTO). See the mapping table there.

---

## Department structure & responsibilities

### 1. AI Planning Department (upstream, pre-existing pipeline)
Owns the customer intent: `requirements/customer_requirements.json`,
`requirements/production_line_plan.json`, `planning/`. It is *not* a reviewer —
it is the source of truth the Chief Engineer reads to frame the review. No agent
in this layer edits it.

### 2. Engineering Department (7 specialists)
The technical core. Each owns one physical domain and may edit the station spec
within that domain only:
- **01 Mechanical** — load paths, frame, brackets, feet. Nothing floats.
- **02 Manufacturing** — DFM/DFA: standard sections, fasteners, part count.
- **03 Electrical** — cabinet, disconnect, power infeed, cabling.
- **04 Pneumatic** — FRL, isolation, solenoid, actuator; a complete air circuit.
- **05 Maintenance** — access, LOTO, covers, service-side fasteners.
- **06 Safety** — e-stop, guards, stack light, markings; **veto authority**.
- **07 Ergonomics** — work height, reach, HMI pose, bin presentation.

### 3. Design Department (1)
- **08 Industrial Designer** — palette, 60/30/10, chamfers, one product family.

### 4. Quality Department (2)
- **12 Quality Assurance Inspector** — external-supplier acceptance audit;
  produces a **punch list**, assigns owners, does **not** fix.
- **09 Factory Operator** — voice-of-user sanity check; flags, minimal edits.

### 5. Management (4)
- **00 Chief Engineer** — reads requirements + specs + prior reviews, writes the
  `engineering_plan`, assigns focus areas. Coordinates; edits no geometry.
- **11 Integration Engineer** — after the specialists, detects and resolves
  cross-discipline conflicts; the only role that may edit the spec to reconcile
  two disciplines.
- **10 CTO Reviewer** — final go/no-go, Unity + presentation readiness; may make
  integration-level fixes only.
- **13 Customer Representative** — checks the result against customer expectation
  (trust, clarity, premium look, usability); edits no geometry.

---

## Data flow

```
customer_requirements.json ─┐
production_line_plan.json  ─┼─► 00 Chief ─► review_outputs/00_engineering_plan_<S>.md
<station>_parameters.json  ─┘                     │ (focus areas)
                                                  ▼
   01→02→03→04→05→06→07→08 each: read specs + all prior review_outputs/*_<S>.md,
   edit its domain in <station>_parameters.json (+ keep _assembly.json in sync),
   rebuild via procedural_builder, validate, write review_outputs/NN_..._<S>.md
                                                  ▼
   09 Operator (flags) ─► 11 Integration (reconciles, edits only for conflicts)
                                                  ▼
   12 QA (punch list) ─► fix loop (routes items back to owning specialists)
                                                  ▼
   10 CTO (gate) ─► 13 Customer (acceptance) ─► release OR next iteration to 00
```

Every modifying step ends in a rebuilt, validated model (0 errors). Reports
accumulate in `review_outputs/` and are read by all downstream roles.

---

## File ownership

| Path | May write | Notes |
|------|-----------|-------|
| `requirements/`, `planning/` | *(nobody in this layer)* | AI Planning is upstream/read-only here |
| `parametric_specs/<station>_parameters.json` | 01–08 (own domain), **11 Integration** (conflict fixes only), 10 CTO (integration-level only) | the geometry-driving spec |
| `parametric_specs/<station>_assembly.json` | same as above | must stay consistent with the parameter file |
| `procedural_builder/`, `generators/` | **nobody** | station-agnostic engine — never edited |
| `design_specs/factory_style_guide.md`, `industrial_rules.json`, `manufacturing_constraints.json` | **nobody** | authority; specs are changed to match them |
| `review_outputs/*.md` | every role writes its own report | punch lists, plans, acceptance |
| `agents/**` (this org layer) | maintained deliberately, not during a station review | |

---

## Decision hierarchy

1. **Customer requirement** defines success (via AI Planning output).
2. **CTO Reviewer** holds final release authority (go / no-go).
3. **Chief Engineer** owns the plan and work assignment.
4. **Integration Engineer** arbitrates cross-discipline conflicts (below CTO).
5. **Safety Engineer** holds an **absolute veto** on any unsafe design — a safety
   blocker cannot be overruled by aesthetics, cost or schedule.
6. Each **specialist** is sovereign within its own domain.

---

## Conflict resolution

When two disciplines' ideal changes collide, the change is decided by the
**priority ladder** (highest wins):

```
safety > mechanical integrity > maintenance > electrical/pneumatics >
ergonomics > manufacturing > visual design > presentation
```

Procedure: the losing agent records a `## Conflict` block naming the other
report and the trade-off; the **Integration Engineer** applies the ladder and
implements the reconciling edit; the **CTO** ratifies. A **safety** finding is
never traded away — it is resolved in safety's favour or the station FAILs.

---

## How this fits into the VEKIFAB pipeline

```
A_Planning (customer req → line plan)
        │
        ▼
WP B geometry:  parametric_specs/<station>_*  ──►  procedural_builder/builder.py
        ▲                                                   │
        │  (edits, within domain, by this org)              ▼
   ┌────┴───────────────────────┐                exports/{blend,glb,screenshots}
   │  AI Engineering Organization│                          │
   │  (this layer, agents/)      │                          ▼
   └─────────────────────────────┘                 Unity walkthrough / digital twin
```

The organization sits **between the planning output and the Unity handoff**: it
takes a built-but-raw station and drives it, through a realistic multi-role
review, to a coherent, safe, serviceable, presentable machine — without ever
touching the renderer or the layout. It is fully reusable across S01–S07; only
the `<station>` spec pair changes.
