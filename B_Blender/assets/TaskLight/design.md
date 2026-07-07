# Task Light — Design Specification

## Purpose
Even, glare-free illumination of a worktop or inspection area.

## Geometry
A slim fixture housing with an emissive LED strip and a real area light.

## Parameters
- `length_m` (0.3-1.5) — Fixture length.

## Materials
- `metal_light`
- `led_white`

## Hierarchy
```
LIGHT_Fixture (box, collider)
  LIGHT_Emitter (box, emissive)
  LIGHT_Lamp (area light, review only)
```

## Connections
- `mount` at (0,0,top), axis +Z — back-rail / overhead mount

## Typical dimensions
0.8 m bar

## Unity collider type
Box (static)

## Physics
Static. Emissive strip; a Blender area light for review is excluded from export.

## LOD importance
low

## Performance budget
~200 tris

## Industrial design notes
Anodised housing, diffused cool-white strip; Unity supplies the actual light.

## Manufacturer inspiration
Generic machine task light in the Waldmann / Banner idiom.
