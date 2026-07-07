# Emergency Stop — Design Specification

## Purpose
Operator safety cut-off; wired into the cell safety chain. Present at every manned station.

## Geometry
A yellow backing plate, a black collar and a red mushroom button facing outward.

## Parameters
- `button_radius_m` (0.02-0.05) — Mushroom head radius.

## Materials
- `safety_yellow`
- `warning_black`
- `led_red`

## Hierarchy
```
ESTOP_Plate (box, collider)
  ESTOP_Collar (cylinder)
  ESTOP_Button (cylinder, emissive)
```

## Connections
- `mount` at (0,0,0), axis +Y — mounts to panel/frame face

## Typical dimensions
160x160 mm plate, Ø 40 mm button

## Unity collider type
Box (static)

## Physics
Static. Interactive trigger in Unity (press event), no rigidbody.

## LOD importance
medium (interactive, close inspection)

## Performance budget
~300 tris

## Industrial design notes
High-contrast red/yellow, twist-release mushroom head, safety pictogram nearby.

## Manufacturer inspiration
Generic e-stop in the Schneider Harmony / Siemens Sirius / EAO idiom.
