# reasoning — AI Reasoning Layer

Explains every engineering decision behind the factory, for presentation and for
Unity information panels. **No geometry; no code changes to the pipeline.**

## Files
- `S0*_reasoning.md` — one document per station, answering 10 questions
  (existence, location, asset choice, dimensions, automation level, safety,
  operator interaction, connections, assumptions, future improvements).
- `factory_reasoning.md` — reasoning behind the whole production line.
- `reasoning_summary.json` — machine-readable per-station reasoning for Unity.

## Unity integration
When the avatar enters a station's info trigger (e.g. `TRIGGER_Info_RobotCell`),
look up the station in `reasoning_summary.json` by its `trigger` field and show
`title`, `summary`, `decision_tree`, `engineering_notes` and `future_improvements`
on the information panel.
