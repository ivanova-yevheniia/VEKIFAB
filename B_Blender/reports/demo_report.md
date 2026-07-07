# VEKIFAB — AI Factory Planner · Demo Report

**Project:** VEKIFAB — AI Factory Planner  
**Use case:** Planner-driven line; Unity assembles the walkthrough  
**Product:** Infusion Pump MF-IP-100  
**Factory area:** 450.0 m² (25.0 × 18.0 m)
**Review score:** 100 / 100

## Key metrics

| Metric | Value |
|--------|-------|
| Stations | 8 |
| Asset instances | 171 |
| Conveyors | 8 |
| Info panels | 8 |
| Physics objects | 39 |
| Collider candidates | 124 |
| Trigger zones | 8 |
| Estimated conveyor length | 12.784 m |
| Avatar route length | 22.0 m |
| Exported files | 20 |

## Asset coverage by category

| Category | Instances |
|----------|-----------|
| cable_management | 2 |
| control | 6 |
| electrical | 7 |
| lighting | 7 |
| logistics | 28 |
| material_handling | 14 |
| robotics | 4 |
| safety | 16 |
| sensor | 3 |
| storage | 12 |
| structure | 64 |
| ux | 8 |

## Generated / exported files

**exports/blend/**
- `01_loading_station.blend`
- `01_loading_station.blend1`
- `02_assembly_station.blend`
- `assembly_station.blend`
- `loading_station.blend`
- `loading_station.blend1`
- `robot_cell.blend`
- `robot_cell.blend1`
- `utils_smoke_test.blend`
**exports/glb/**
- `01_loading_station.glb`
- `02_assembly_station.glb`
- `assembly_station.glb`
- `loading_station.glb`
- `robot_cell.glb`
- `utils_smoke_test.glb`
**exports/screenshots/**
- `01_loading_station.png`
- `02_assembly_station.png`
- `assembly_station.png`
- `loading_station.png`
- `robot_cell.png`

## The AI pipeline

customer requirements → process plan → asset composition → procedural builder → Blender → Unity avatar walkthrough

1. **Customer requirements** — the client's production needs (`requirements/customer_requirements.json`).
2. **Process plan** — the ordered line of stations (`requirements/production_line_plan.json`, `factory_description.json`).
3. **Asset composition** — each station composed as a bill of reusable industrial assets (`composer/`, `assets/`).
4. **Procedural builder** — the generic JSON-driven renderer (`procedural_builder/`) turns specs into geometry.
5. **Blender** — exports `.blend` / `.glb` with Unity-ready colliders, triggers and tags.
6. **Unity avatar walkthrough** — an avatar walks the line and inspects each station via info-panel triggers.
