# Factory Reasoning — VEKIFAB — AI Factory Planner

*Product: Compact Medical Infusion Pump (MF-IP-100) · Floor: 25 x 18 m · Target: 480 units/day (single 8 h shift, ~60 s cycle)*

## Why this line, this way

The line is a **hybrid semi-automated cell line** sized to a modest medical-device
throughput (480/day). At that volume a fully automated line is not justified, so
**humans are kept where they add most value** (dexterous kitting, assembly and
packaging) and **automation is placed where it pays off** (precise robotic
handling, objective vision inspection, and functional test).

## Layout logic
Stations are arranged **linearly along +X** at a common y so material flows in one
direction: `S01 Loading → S02 Assembly → S03 Robot Cell → S04 Vision → S05 Test →
S06 Packaging → S07 Storage`. A **pedestrian walkway runs parallel (+Y)** so the
Unity avatar — and real operators — can inspect every station without entering a
process zone.

## Automation & safety escalation
Automation and guarding **escalate only where needed**: open manual benches for
S01/S02/S06 (e-stop + stack light), automated but enclosed optics/fixtures for
S04/S05, and **full fencing only at the robot cell (S03)**, the single moving-hazard
station. Storage (S07) is an unmanned buffer.

## Flow & buffering
Powered roller conveyors connect every adjacent pair (C01–C06). S01 buffers kits so
assembly is never starved; S07 buffers finished goods so the line runs while
dispatch batches. Quality gates (vision, test) sit **before** packaging so only
good units are shipped, with per-serial traceability for the medical context.

## Architecture reasoning
Every station is composed from a **shared industrial asset library** (frames, feet,
conveyors, bins, cabinets, HMIs, stack lights, e-stops, fences, robot assets…) under
one style guide and material palette, so the whole plant reads as one modern smart
factory and new stations are authored as **asset compositions, not bespoke geometry**.

## Key assumptions
Palletized inbound components; a ~60 s balanced cycle; a single shift; manual
assembly feasible in cycle; medical traceability required; one-shift finished-goods
buffer.

## Future direction
Raise automation as volume grows: AMR infeed, cobot-assisted assembly, vision-guided
robotics, parallel test nests, automatic case packing and ASRS storage with WMS/MES
integration.
