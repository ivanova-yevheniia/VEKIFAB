# Electrical Cabinet — Design Specification

## Purpose
Houses the PLC, IO and power for a station; the electrical hub of the cell.

## Geometry
A box enclosure with a hinged door, handle and a green power indicator.

## Parameters
- `height_m` (0.4-2.0) — Cabinet height.
- `width_m` (0.3-1.2) — Cabinet width.

## Materials
- `metal_light`
- `metal_dark`
- `led_green`

## Hierarchy
```
CAB_Body (box, collider)
  CAB_Door (box)
  CAB_Handle (box)
  CAB_PowerLed (cylinder)
```

## Connections
- `floor` at (0,0,0), axis -Z — floor/frame mount
- `gland` at (0,0,bottom), axis -Z — cable entry

## Typical dimensions
600x400x800 mm

## Unity collider type
Box (static)

## Physics
Static. Door hinge available for articulation; no rigidbody.

## LOD importance
medium

## Performance budget
~600 tris

## Industrial design notes
RAL-grey powder coat, gland plate, latch handle, small DIN-rail hint through a window.

## Manufacturer inspiration
Generic enclosure in the Rittal / Eldon / Siemens idiom.
