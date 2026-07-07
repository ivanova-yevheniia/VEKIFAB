# Barcode Scanner — Design Specification

## Purpose
Reads part / carton serial codes for traceability at inspection, test and packaging.

## Geometry
A compact body with a red-emissive lens window and an L bracket.

## Parameters
- `mount_angle_deg` (-45 to 45) — Reader aim angle.

## Materials
- `warning_black`
- `led_red`
- `metal_dark`

## Hierarchy
```
SCAN_Body (box, collider)
  SCAN_Lens (cylinder, emissive)
  SCAN_Bracket (box)
```

## Connections
- `bracket` at (0,0.03,-0.05), axis +Y — bracket/arm mount

## Typical dimensions
80x60x50 mm

## Unity collider type
Box (static)

## Physics
Static. Emissive read window; sensor trigger in Unity.

## LOD importance
low

## Performance budget
~250 tris

## Industrial design notes
Dark housing, red aiming window, sturdy bracket, small status LED.

## Manufacturer inspiration
Generic code reader in the Cognex / SICK / Keyence idiom.
