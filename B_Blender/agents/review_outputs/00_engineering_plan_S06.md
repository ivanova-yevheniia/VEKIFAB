# 00 — Engineering Plan — S06 Packaging

- **Chief Engineer** · Station S06 `STATION_06_Packaging` @ world [19.17, 6.12, 0].
- S06 had no `parametric_specs` geometry — authoring `packaging_parameters.json` +
  `packaging_assembly.json` from the composition (exact footprint, layout, Unity names).

## Objective
Visitor understands in <5 s: **device finished → packed → label printed → box sealed →
ready for warehouse.** Preserve names/footprint; ≤20k tris, ≤16 materials; every part
answers mounted/made/serviced/powered/adjusted; only real industrial engineering.

## Preserved architecture (composition)
Legs ±0.8/±0.6, feet, roller conveyors ±1.9, info world y8.52, stack [0.9,-0.8], e-stop
[-1.05,-0.7], cabinet [-1.2,-0.5], task [0,-0.55,2.15], pallet [0.5,0.6], HMI [0.85,-0.5],
cartons `PHYS_Packaging_Box_1..4`.

## Process line (left→right, +X) on the worktop
carton magazine (folded blanks) → box erector (OpenBox) → packing nest + foam insert +
device (InsertProduct) + leaflet → carton closer (CloseBox) → tape dispenser + roll →
thermal label printer + roll + maintenance door (PrintLabel) → label applicator
(ApplyLabel) → barcode scanner + verification camera (BarcodeScan) → finished carton →
output conveyor → warehouse; reject box + pusher (Reject) for fails.

## Discipline focus
01 frame/worktop/uprights/feet · 02 fixtures + adjustable guides + box stops · 03 cabinet
DIN (PLC + printer controller + PSU) + cabling + M12 · 04 FRL + pneumatic cylinders +
tubing on erector/closer/applicator/reject · 05 printer maintenance door + service access +
calibration labels + asset ID · 06 e-stop + stack + start + markings · 07 operator zone +
mat + HMI pose · 08 palette/accent · 11/12/10/13 integrate/QA/gate/accept.

## Acceptance bar
Full pack chain visible; HMI shows Packaging Station / Label Printed / Serial Number / Box
OK / Cycle Time; all 7 Unity placeholders present; finished cartons on the pallet; 0 errors.
