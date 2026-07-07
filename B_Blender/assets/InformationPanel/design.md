# Information Panel — Design Specification

## Purpose
Presents the station description to the walkthrough avatar; carries the Unity info trigger.

## Geometry
A white board on a post with title/body text and a wireframe trigger volume in front.

## Parameters
- `board_height_m` (1.2-2.0) — Board centre height.
- `wrap_chars` (20-40) — Body word-wrap width.

## Materials
- `white_panel`
- `warning_black`
- `metal_dark`

## Hierarchy
```
INFO_Board (panel, collider)
  INFO_Title (text)
  INFO_Body (text)
  INFO_Post (cylinder)
  TRIGGER_Info (box, trigger)
```

## Connections
- `floor` at (0,0,0), axis -Z — floor mount (post)
- `faces` at board front, axis +Y — reads from the walkway

## Typical dimensions
1200x700 mm board at ~1.6 m height

## Unity collider type
Box (static) + Box (trigger)

## Physics
Static board; a non-blocking trigger volume fires the info event in Unity.

## LOD importance
medium

## Performance budget
~300 tris (+ text)

## Industrial design notes
White board, black high-contrast text, sans-serif; text converted to mesh for glTF.

## Manufacturer inspiration
Generic industrial signage / andon board.
