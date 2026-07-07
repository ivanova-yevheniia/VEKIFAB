# Stack Light — Design Specification

## Purpose
At-a-glance station status (running / warning / fault); the andon signal of the cell.

## Geometry
A base, a short pole and three stacked emissive segments capped by a dome.

## Parameters
- `segment_count` (2-5) — Number of light segments.

## Materials
- `metal_dark`
- `led_red`
- `led_amber`
- `led_green`
- `warning_black`

## Hierarchy
```
STACK_Base (cylinder, collider)
  STACK_Pole (cylinder)
  STACK_Segment_* (emissive)
  STACK_Dome
```

## Connections
- `mount` at (0,0,0), axis +Z — mounts on frame top / pole

## Typical dimensions
Ø 60 mm, 0.25-0.3 m tall

## Unity collider type
Box (static)

## Physics
Static. Emissive segments (active segment strongly lit).

## LOD importance
low

## Performance budget
~500 tris

## Industrial design notes
Translucent coloured segments, only the active one bright; classic red/amber/green order.

## Manufacturer inspiration
Generic signal tower in the Patlite / Werma / Banner idiom.
