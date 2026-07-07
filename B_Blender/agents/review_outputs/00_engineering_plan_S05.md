# 00 — Engineering Plan — S05 Functional Test

- **Reviewer:** 00 Chief Engineer · **Station:** S05 `STATION_05_FunctionalTest` @ world [16.5, 6.0, 0]
- **Note:** S05 had no `parametric_specs` geometry — only a composition + reasoning. This
  pass authors `functional_test_parameters.json` + `functional_test_assembly.json` from
  the composition (exact footprint, layout, Unity names) and builds it to hero quality.

## Objective ("done")
A visitor understands in <5 s: **assembled device enters → auto functional test (flow /
pressure / voltage / current / leak) → PASS or FAIL → sent to packaging**. Preserve
composition names, footprint, layout; ≤20k tris, ≤16 materials; every part answers
mounted/made/serviced/powered/adjusted; only real industrial engineering, no decoration.

## Preserved architecture (from composition)
Legs ±0.85/±0.6, feet, roller conveyors ±1.875, info panel world y8.6, e-stop [-1.05,-0.7],
stack light [0.9,-0.8], task light [0,-0.55,2.15], cabinet [-1.2,-0.5], HMI [0.85,-0.5],
scanner [0.3,-0.5], device `PHYS_FunctionalTest_Box_1` [-0.2,-0.5].

## Assignments
- **01** frame + reinforced worktop + back uprights + gussets + feet; nothing floats.
- **02** DFM: precision fixture plate, locating pins, bushings, standard fasteners.
- **03** controller cabinet DIN interior (PLC + DAQ + IPC + PSU), cabling, glands, M12.
- **04** pneumatics: FRL, regulators, valves, tubing, pneumatic locking clamps + QD couplings.
- **05** maintenance: access panels, service labels, calibration stickers, asset ID plate.
- **06** safety: e-stop, stack light, two-hand/guarded start, PASS/FAIL andon, markings.
- **07** ergonomics: operator zone, HMI pose, mat.
- **08** design: canonical palette, blue accent discipline, hero = fixture + dock.
- **11/12/10/13** integrate, QA punch list, CTO gate, customer accept.

## Acceptance bar
Test process legible; measurement modules (pressure/flow/V-I/leak) visible; pogo-pin
connector docking + probes present; HMI shows Functional Test / PASS / Flow OK / Pressure
OK / Voltage OK / Current OK / Cycle 8.2 s; all Unity placeholders present; 0 build errors.
