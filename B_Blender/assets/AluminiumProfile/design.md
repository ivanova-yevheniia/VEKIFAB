# Aluminium Profile — Design Specification

## Purpose
Load-bearing structural member; the universal building block for bench, cell, fence and rack frames.

## Geometry
A straight extruded bar, near-square section, chamfered edges, optional T-slot grooves on faces. Single beveled box.

## Parameters
- `length_m` (0.1-6.0) — Bar length along local X.
- `section_mm` ([20, 40, 45, 80]) — Square section size.
- `slot_detail` (True) — Show T-slot grooves.

## Materials
- `metal_light`

## Hierarchy
```
PROFILE_Beam (box, collider)
  slot detail (optional inset)
```

## Connections
- `end_a` at (-L/2,0,0), axis -X — butt/bracket joint
- `end_b` at (+L/2,0,0), axis +X — butt/bracket joint
- `face_slot` at each face, axis +/-Y,+/-Z — T-slot mount

## Typical dimensions
0.1-6.0 m length, 40x40 mm section

## Unity collider type
Box (static)

## Physics
Static, non-movable. No rigidbody; carries other assets.

## LOD importance
high (most repeated element in the plant)

## Performance budget
~200 tris (24 without slot detail)

## Industrial design notes
Anodised matte finish, visible T-slots, black slot covers, end caps. Small but present chamfers.

## Manufacturer inspiration
Generic slot-profile framing in the language of Bosch Rexroth, item and Festo — nothing copied.
