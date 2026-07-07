# HMI Panel — Design Specification

## Purpose
Displays line status and pick-to-light / work guidance; the operator interface at a station.

## Geometry
A dark emissive screen, a metal bezel and a row of hardware buttons.

## Parameters
- `diagonal_in` (10-24) — Screen diagonal (inches).
- `tilt_deg` (-20 to 0) — Forward tilt.

## Materials
- `screen_dark`
- `metal_dark`
- `blue_accent`

## Hierarchy
```
HMI_Screen (panel, collider, emissive)
  HMI_Bezel (box)
  HMI_Button_* (cylinders)
```

## Connections
- `mount` at (0,0,0), axis +Y — arm/pole or panel mount

## Typical dimensions
300x220 mm active area, ~15-22 inch class

## Unity collider type
Box (static)

## Physics
Static. Emissive screen; interactive UI surface in Unity.

## LOD importance
medium

## Performance budget
~400 tris

## Industrial design notes
Thin bezel, dark glass, subtle self-illumination, one hardware button row.

## Manufacturer inspiration
Generic HMI in the Siemens SIMATIC / Beckhoff CP / B&R idiom.
