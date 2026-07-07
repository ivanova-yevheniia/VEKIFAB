# 00 — Engineering Plan — S07 Storage (Warehouse Dispatch)

- **Chief Engineer** · Station S07 `STATION_07_Storage` @ world [22.5, 6.12, 0], envelope 3.5×3.5×3.0.
- No `parametric_specs` existed — authoring `storage_parameters.json` + `storage_assembly.json`
  from the composition (footprint, layout, Unity names preserved).

## Objective (5-second read)
finished products → **warehouse** (pallet rack) → **inventory** (HMI + inventory display) →
**shipment** (weigh + barcode/RFID portal → shipping). Reads as the warehouse END of the line.

## Preserved architecture (composition)
Legs ±0.8/±0.6, feet, input roller conveyor −1.9, info world y8.52, stack [0.9,-0.8],
pallets `STATION_07_Storage_Pallet_1..4` [-0.6,0]/[0.3,0]/[-0.6,0.5]/[0.3,0.5], cartons
`PHYS_Storage_Box_1..8` on the staging table. Add cabinet, HMI, e-stop (per brief).

## Layout
Back (−Y): **pallet rack** (hero) — 3 upright frames, load beams (2 levels), anchor plates +
bolts, cross bracing, loaded pallets + cartons, location/shelf numbering. Centre: dispatch
staging table (8 finished cartons). Front (+Y): pallet loading zone (4 floor pallets, 2
loaded). +X: **barcode/RFID portal** + **weighing platform** → shipping. −X: input conveyor +
cabinet. HMI + inventory display front-right.

## Discipline focus
01 rack + table structure, anchor plates, bracing · 02 pallet positioning guides, stops ·
03 cabinet DIN + disconnect + cabling · 05 maintenance access + service labels · 06 e-stop,
stack, markings · 08 palette (orange-blue racking accent stays within blue_accent) · signage:
pallet labels, shelf/location numbering, QR/barcode signs, shipping + loading zones.

## Acceptance bar
Rack dominant + loaded; barcode/RFID portal + weighing visible; HMI shows Warehouse Storage /
Location A03 / Inventory / Pallet Ready / Dispatch Queue; all 7 Unity placeholders present; 0 errors.
