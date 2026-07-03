# AI Engineering Assistant — Technisches Fundament (MVP)

> Modul: Virtual Engineering / Open Engineering Metaverse
> Team: 3 Studierende · Zeitrahmen: wenige Entwicklungssessions (Abende)
> Ziel: **beeindruckender, professionell wirkender MVP mit Live-Demo** — kein Forschungsprototyp.
> Basiert lose auf: Tinsel et al., *"Concept of an initial requirements-driven factory layout planning and synthetic expert verification for industrial simulation based on LLM"* (ISW, Universität Stuttgart).

---

## 0. Leitprinzipien (CTO-Entscheidungen)

Diese Regeln gelten für **jede** technische Entscheidung im Projekt:

1. **JSON-Verträge statt geteiltem Code.** Module reden ausschließlich über JSON-Dateien. So kann jeder unabhängig arbeiten und wir integrieren erst am Schluss.
2. **Mock zuerst, echt später.** Jedes Modul startet mit einer statischen Beispiel-JSON. Iteration 1 läuft end-to-end mit Mocks.
3. **Fertige Bausteine nutzen.** Anthropic Claude API (Denkleistung), Blender-MCP (3D), Streamlit (UI). Wir bauen nur den Klebstoff.
4. **Dumme Algorithmen sind erlaubt.** Greedy-Grid-Placement statt Optimierer. Regelbasierte Validierung statt Solver. Das Publikum sieht das Ergebnis, nicht den Algorithmus.
5. **Der Wow-Faktor ist die 3D-Fabrik + der Chat.** Dort investieren wir die Politur-Zeit, nicht in „korrekte" Fabrikplanung.

---

## 1. Projektvision

**Ein Ingenieur beschreibt in normaler Sprache, was produziert werden soll — und Sekunden später steht die begehbare 3D-Fabrik im Open Engineering Metaverse.**

Heute dauert das Erstellen erster Fabrik- und Simulationsmodelle Wochen manueller Arbeit. Unser AI Engineering Assistant automatisiert den kompletten Weg von *unstrukturierten Kundenanforderungen* bis zu einer *validierten, interaktiven 3D-Fabrikszene*:

```
"Ich will 50.000 Aluminium-Gehäuse pro Jahr fräsen, entgraten und lackieren."
        ↓  (Sekunden)
   Vollständige 3D-Fabrik in Blender — Maschinen platziert, Wege frei,
   Layout validiert, per Chat live veränderbar.
```

**Elevator Pitch:** *„Cursor für Fabrikplanung."* Natürliche Sprache rein, begehbare, validierte Fabrik raus — inklusive KI-Experte, der das Layout gegenprüft.

**Abgrenzung zum Paper:** Das ISW-Paper endet beim Import in ein Simulationswerkzeug. Wir erweitern es um (a) **interaktive Chat-Bearbeitung** der Szene und (b) **Visualisierung im Open Engineering Metaverse** via Blender.

---

## 2. Scope

### ✅ Gehört zum MVP

| # | Feature |
|---|---------|
| 1 | Chat-UI: Nutzer gibt Anforderungen in natürlicher Sprache ein |
| 2 | LLM extrahiert Produkt, Stückzahl, Prozessschritte → `factory.json` |
| 3 | Maschinenauswahl aus statischem Katalog (~15 Maschinentypen) |
| 4 | Automatisches 2D-Layout (Greedy-Grid) → `layout.json` |
| 5 | Regelbasierte Validierung (+ optionaler „synthetischer Experte" per LLM) → `validation.json` |
| 6 | 3D-Szene in Blender via MCP (Boxen/Primitive, später echte Assets) → `scene.json` |
| 7 | Interaktive Änderungen per Chat („mach die Halle breiter", „füge eine zweite Fräse hinzu") |
| 8 | Live-Viewport-Screenshot / begehbare Blender-Szene für die Präsentation |

### ❌ Gehört ausdrücklich NICHT zum MVP

- ❌ Echte physikalische Materialfluss-Simulation (keine Diskrete-Event-Simulation)
- ❌ Optimale Layout-Optimierung (kein OR-Solver, keine Metaheuristik)
- ❌ Persistente Datenbank / User-Accounts / Multi-Tenant
- ❌ Echte Maschinen-Datenbank / Herstellerkataloge / Preis-APIs
- ❌ Kollisionsfreie Roboter-Pfadplanung, Kinematik, Physik
- ❌ CAD-Import, DXF/STEP-Verarbeitung
- ❌ Deployment, Auth, CI/CD, Skalierung, Docker-Cluster
- ❌ VR-Headset-Integration (nur Blender-Viewport; VR ist „Future Work"-Folie)
- ❌ Feingranulare 3D-Modelle mit korrekten Maschinen-Geometrien (Primitive genügen)

> **Faustregel:** Wenn ein Feature nicht in der 5-Minuten-Demo sichtbar ist, gehört es nicht in den MVP.

---

## 3. Systemarchitektur

### 3.1 Gesamtüberblick

```
┌──────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Streamlit)                           │
│   Chat-Eingabe  ·  JSON-Anzeige  ·  Blender-Viewport-Screenshot       │
└───────────────────────────────┬──────────────────────────────────────┘
                                 │  HTTP (REST/JSON)
┌───────────────────────────────▼──────────────────────────────────────┐
│                      ORCHESTRATOR (FastAPI)                            │
│         Steuert die Pipeline · hält Zustand · routet Chat             │
└──┬─────────┬──────────┬───────────┬──────────┬───────────────────────┘
   │         │          │           │          │
   ▼         ▼          ▼           ▼          ▼
┌──────┐ ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐
│ M1   │ │  M2    │ │  M3    │ │   M4     │ │   M5     │
│Req.  │ │Machine │ │Layout  │ │Validator │ │ Scene    │
│Analyzer│Selector│ │Gen.    │ │(+Expert) │ │ Builder  │
└──┬───┘ └───┬────┘ └───┬────┘ └────┬─────┘ └────┬─────┘
   │         │          │           │            │
   │ factory.json  layout.json validation.json  │ scene.json
   ▼         ▼          ▼           ▼            ▼
┌──────────────────────┐              ┌────────────────────────┐
│  Anthropic Claude API │              │   Blender  (via MCP)   │
│  (M1, M2, M4-Expert)  │              │   Socket-Addon         │
└──────────────────────┘              └────────────────────────┘
```

### 3.2 Datenfluss (Happy Path)

```
Nutzer-Text
   │
   ▼  M1 Requirements Analyzer  (LLM)
factory.json  ──►  M2 Machine Selector  (Katalog + LLM)
   │                    │
   │                    ▼  M3 Layout Generator  (Greedy-Grid)
   │                layout.json
   │                    │
   │                    ▼  M4 Validator  (Regeln + LLM-Experte)
   │                validation.json
   │                    │
   │                    ▼  M5 Scene Builder  (Blender-MCP)
   │                scene.json  ──►  Blender-Viewport
   ▼
Antwort + Screenshot an Nutzer
```

### 3.3 Interaktiver Änderungs-Loop (Iteration 4)

```
Nutzer: "Füge eine zweite Fräse hinzu"
   │
   ▼  Orchestrator: LLM klassifiziert Änderung → betroffenes Modul
   │
   ├─ betrifft Maschinen? → M2 → M3 → M4 → M5 (Teil-Rerun)
   └─ betrifft nur Layout? → M3 → M4 → M5
   │
   ▼  Neuer Screenshot + kurze Erklärung an Nutzer
```

**Kern-Designentscheidung:** Der Orchestrator ist ein **dünner Zustandshalter**. Er hält das aktuelle `factory.json`/`layout.json` im Speicher und ruft bei Änderungen nur die betroffenen Module neu auf. Kein State außerhalb des Prozesses (In-Memory reicht für die Demo).

---

## 4. Repositorystruktur (GitHub)

```
ai-engineering-assistant/
├── README.md                 # Pitch, Screenshot/GIF, Quickstart, Team
├── LICENSE                   # MIT
├── .gitignore                # python, venv, .env, __pycache__, blend1
├── .env.example              # ANTHROPIC_API_KEY=...
├── pyproject.toml            # Abhängigkeiten (uv/poetry), ein Paket
├── docs/
│   ├── PROJEKT_FUNDAMENT.md  # dieses Dokument
│   ├── architecture.png      # Diagramm aus Abschnitt 3
│   └── demo-script.md        # Abschnitt 12 als Standalone
├── data/
│   ├── machine_catalog.json  # statischer Maschinenkatalog (M2)
│   └── examples/             # Beispiel-Requests für Demo & Tests
├── schemas/                  # JSON-Schemas (Abschnitt 7) — der Vertrag!
│   ├── factory.schema.json
│   ├── layout.schema.json
│   ├── validation.schema.json
│   └── scene.schema.json
├── src/
│   └── aiea/
│       ├── __init__.py
│       ├── config.py         # API-Keys, Pfade, Konstanten
│       ├── models.py         # Pydantic-Modelle zu den Schemas
│       ├── orchestrator.py   # FastAPI-App + Pipeline
│       ├── modules/
│       │   ├── m1_requirements.py
│       │   ├── m2_machines.py
│       │   ├── m3_layout.py
│       │   ├── m4_validator.py
│       │   └── m5_scene.py
│       └── llm.py            # dünner Claude-API-Wrapper
├── app/
│   └── streamlit_app.py      # Frontend
├── tests/
│   └── test_contracts.py     # prüft: erfüllen Mock-JSONs die Schemas?
└── mocks/                    # Fixe Beispiel-Outputs pro Modul (Iteration 1!)
    ├── factory.mock.json
    ├── layout.mock.json
    ├── validation.mock.json
    └── scene.mock.json
```

**Warum diese Struktur:**
- `schemas/` + `mocks/` sind das Herzstück der Parallelarbeit — sie existieren ab Tag 1.
- Jedes Modul ist **eine Datei** in `modules/`. Ein Modul = wenige Stunden.
- `data/machine_catalog.json` ersetzt einen echten Datensatz.

---

## 5. Ordnerstruktur — Verantwortlichkeiten

| Ordner | Inhalt | Owner |
|--------|--------|-------|
| `schemas/` | JSON-Verträge (gemeinsam vereinbart) | **Alle** (Tag 1) |
| `mocks/` | Beispiel-Outputs für unabhängiges Arbeiten | **Alle** (Tag 1) |
| `src/aiea/modules/m1,m2` | LLM-Analyse & Maschinenwahl | **Person A** |
| `src/aiea/modules/m3,m4` | Layout & Validierung | **Person B** |
| `src/aiea/modules/m5` + `app/` | 3D-Szene & Frontend | **Person C** |
| `src/aiea/orchestrator.py` | Pipeline-Glue | **Person A** (leitend) |
| `data/`, `docs/`, `tests/` | Katalog, Doku, Vertragstests | geteilt |

---

## 6. Module

> Jedes Modul ist eine reine Funktion: **JSON rein → JSON raus**. Kein verstecktes Wissen, kein geteilter Zustand. Dadurch testbar und parallel entwickelbar.

### M1 — Requirements Analyzer
- **Zweck:** Unstrukturierten Nutzertext in strukturierte Anforderungen + Prozessschritte übersetzen.
- **Input:** `str` (Freitext des Nutzers)
- **Output:** `factory.json`
- **Verantwortlichkeit:** Produkt, Material, Jahresstückzahl und die geordnete Liste der Fertigungsschritte erkennen. Fehlende Angaben mit sinnvollen Defaults füllen und markieren.
- **Umsetzung:** Ein Claude-Aufruf mit **Tool-Use / structured output**, der direkt gegen `factory.schema.json` validiert. Kein Parsing-Code.
- **Schnittstelle:** `analyze(text: str) -> Factory`

### M2 — Machine Selector
- **Zweck:** Jedem Prozessschritt eine konkrete Maschine aus dem Katalog zuordnen.
- **Input:** `factory.json`
- **Output:** `factory.json` (angereichert um `machines[]` mit Abmessungen)
- **Verantwortlichkeit:** Passenden Maschinentyp wählen, Anzahl aus Stückzahl/Taktzeit grob abschätzen, Footprint (L×B×H) aus dem Katalog übernehmen.
- **Umsetzung:** Regelbasiertes Matching (`process_type → machine_type`) über `machine_catalog.json`; Mengen-Heuristik `ceil(annual_volume / machine_capacity)`. LLM nur als Fallback für unbekannte Schritte.
- **Schnittstelle:** `select_machines(factory: Factory) -> Factory`

### M3 — Layout Generator
- **Zweck:** Maschinen kollisionsarm auf einer Hallenfläche anordnen.
- **Input:** `factory.json` (mit Maschinen)
- **Output:** `layout.json`
- **Verantwortlichkeit:** Position (x, y), Rotation und Gangbreiten festlegen; Reihenfolge = Prozessfluss (Fließbandlogik).
- **Umsetzung:** **Greedy-Grid** — Maschinen in Prozessreihenfolge in Reihen platzieren, feste Gangbreite (z. B. 2 m) dazwischen, Hallengröße aus Summe der Footprints + Puffer ableiten. Keine Optimierung.
- **Schnittstelle:** `generate_layout(factory: Factory) -> Layout`

### M4 — Layout Validator (+ Synthetischer Experte)
- **Zweck:** Layout auf Plausibilität prüfen und Feedback geben.
- **Input:** `layout.json` (+ `factory.json`)
- **Output:** `validation.json`
- **Verantwortlichkeit:** Harte Regeln (Überlappungen, Mindest-Gangbreite, Maschinen in Halle) **plus** eine LLM-„Experten"-Zweitmeinung (fehlt ein typischer Schritt? passt die Reihenfolge?).
- **Umsetzung:** Teil A = einfache Geometrie-Checks (Bounding-Box-Overlap). Teil B = ein Claude-Aufruf im Stil des Paper-„synthetic expert": *„Bewerte dieses Fabriklayout, nenne Risiken."* Ausgabe als Ampel + Findings-Liste.
- **Schnittstelle:** `validate(layout: Layout, factory: Factory) -> Validation`

### M5 — Scene Builder
- **Zweck:** Layout in eine 3D-Blender-Szene übersetzen.
- **Input:** `layout.json` (+ `validation.json` für Farbcodierung)
- **Output:** `scene.json` + **live erzeugte Blender-Szene**
- **Verantwortlichkeit:** Halle (Boden + Wände), pro Maschine ein Objekt (Iteration 1: skalierte Box mit Label; später Poly-Haven/Sketchfab-Asset), Farbe nach Maschinentyp/Validierungsstatus, Kamera setzen.
- **Umsetzung:** `scene.json` beschreibt Objekte deklarativ; ein Übersetzer schickt sie über den **Blender-MCP** (`execute_blender_code` / Asset-Download) an Blender. Kein manuelles Blender-Scripting nötig — der MCP macht die Arbeit.
- **Schnittstelle:** `build_scene(layout: Layout, validation: Validation) -> Scene`

### Orchestrator (kein „Modul", aber zentral)
- **Zweck:** Pipeline verdrahten, Zustand halten, Chat-Änderungen routen.
- **Input:** HTTP-Requests vom Frontend.
- **Output:** JSON-Antworten + Screenshot-URL.
- **Schnittstellen (REST):** siehe Abschnitt 8.

---

## 7. JSON-Schemas

> Vereinfachte, aber vollständige Verträge. In `schemas/` als JSON-Schema ablegen und mit Pydantic spiegeln (`src/aiea/models.py`). **Diese vier Dateien sind der wichtigste Artefakt des Projekts** — sie werden an Tag 1 gemeinsam festgezurrt.

### 7.1 `factory.json`
```json
{
  "project_name": "Aluminium-Gehäusefertigung",
  "product": {
    "name": "Aluminium-Gehäuse",
    "material": "aluminium",
    "annual_volume": 50000
  },
  "process_steps": [
    { "id": "s1", "name": "Fräsen",    "process_type": "milling",   "order": 1 },
    { "id": "s2", "name": "Entgraten", "process_type": "deburring", "order": 2 },
    { "id": "s3", "name": "Lackieren", "process_type": "painting",  "order": 3 }
  ],
  "machines": [
    {
      "id": "m1",
      "for_step": "s1",
      "type": "cnc_mill",
      "label": "CNC-Fräsmaschine",
      "count": 2,
      "footprint_m": { "length": 3.0, "width": 2.5, "height": 2.8 },
      "capacity_per_year": 30000
    }
  ],
  "assumptions": ["Taktzeit aus Standardwerten geschätzt"],
  "meta": { "created_by": "M1", "version": 1 }
}
```

### 7.2 `layout.json`
```json
{
  "hall": { "width_m": 20.0, "length_m": 30.0, "aisle_width_m": 2.0 },
  "placements": [
    {
      "machine_id": "m1",
      "instance": 1,
      "type": "cnc_mill",
      "label": "CNC-Fräsmaschine",
      "position_m": { "x": 3.0, "y": 4.0 },
      "rotation_deg": 0,
      "footprint_m": { "length": 3.0, "width": 2.5, "height": 2.8 }
    }
  ],
  "flow_path": [ { "x": 3.0, "y": 4.0 }, { "x": 9.0, "y": 4.0 } ],
  "meta": { "created_by": "M3", "algorithm": "greedy_grid", "version": 1 }
}
```

### 7.3 `validation.json`
```json
{
  "status": "warning",                         
  "score": 0.78,
  "hard_checks": [
    { "rule": "no_overlap",        "passed": true,  "detail": "" },
    { "rule": "min_aisle_width",   "passed": true,  "detail": "" },
    { "rule": "inside_hall",       "passed": true,  "detail": "" }
  ],
  "expert_findings": [
    { "severity": "warning", "message": "Nach dem Lackieren fehlt üblicherweise ein Trockenofen." },
    { "severity": "info",    "message": "Prozessreihenfolge ist plausibel." }
  ],
  "meta": { "created_by": "M4", "version": 1 }
}
```
`status ∈ {ok, warning, error}` · `severity ∈ {info, warning, error}`

### 7.4 `scene.json`
```json
{
  "scene_name": "factory_v1",
  "hall": { "width_m": 20.0, "length_m": 30.0, "wall_height_m": 4.0 },
  "objects": [
    {
      "id": "m1_1",
      "kind": "machine",
      "asset": "box",                    
      "type": "cnc_mill",
      "label": "CNC-Fräsmaschine",
      "position_m": { "x": 3.0, "y": 4.0, "z": 0.0 },
      "size_m": { "length": 3.0, "width": 2.5, "height": 2.8 },
      "rotation_deg": 0,
      "color": "#3B82F6",                 
      "status": "ok"
    }
  ],
  "camera": { "position_m": { "x": 10, "y": -15, "z": 12 }, "look_at": { "x": 10, "y": 15, "z": 0 } },
  "meta": { "created_by": "M5", "version": 1 }
}
```
`asset` = `"box"` (Iteration 1) oder Asset-Referenz (Poly Haven / Sketchfab, spätere Iteration). `color` codiert Maschinentyp oder Validierungsstatus (grün/gelb/rot).

---

## 8. API zwischen den Modulen

### 8.1 Interne Modul-Signaturen (Python)
```python
analyze(text: str)                         -> Factory        # M1
select_machines(factory: Factory)          -> Factory        # M2
generate_layout(factory: Factory)          -> Layout         # M3
validate(layout: Layout, factory: Factory) -> Validation     # M4
build_scene(layout: Layout, val: Validation) -> Scene        # M5
```
Alle Typen sind Pydantic-Modelle = 1:1 zu den Schemas. Ein Modul kennt **nur** seine Input- und Output-Typen.

### 8.2 REST-API (Orchestrator ↔ Frontend)

| Methode | Endpoint | Body | Antwort |
|---------|----------|------|---------|
| `POST` | `/api/generate` | `{ "text": "..." }` | `{ factory, layout, validation, scene, screenshot_url }` |
| `POST` | `/api/modify` | `{ "instruction": "..." }` | wie oben (aktualisiert) |
| `GET`  | `/api/state` | – | aktueller Pipeline-Zustand |
| `GET`  | `/api/screenshot` | – | aktueller Blender-Viewport (PNG) |
| `GET`  | `/health` | – | `{ "status": "ok" }` |

**`/api/generate`** durchläuft M1→M5 komplett. **`/api/modify`** lässt Claude die Instruktion klassifizieren und startet nur die betroffenen Module neu. Der gesamte Zustand liegt in-memory im Orchestrator (eine Session — für die Demo ausreichend).

---

## 9. Roadmap — 5 Iterationen à ein Abend

> **Prinzip:** Iteration 1 ist bereits **komplett lauffähig** (mit Mocks). Jede weitere Iteration ersetzt einen Mock durch echte Logik. Zu jedem Zeitpunkt ist die Demo vorführbar.

### Iteration 1 — „Es läuft end-to-end" (Skelett + Mocks)
- Repo, Schemas, Mocks, FastAPI-Grundgerüst, Streamlit-Chat.
- Jedes Modul gibt seine **Mock-JSON** zurück.
- M5 zeichnet die Mock-Boxen echt in Blender über MCP.
- **Ergebnis:** Text eintippen → Boxen erscheinen in Blender. Pipeline steht.

### Iteration 2 — „Die KI versteht" (echtes M1 + M2)
- M1: echter Claude-Call mit structured output → `factory.json`.
- M2: `machine_catalog.json` (~15 Maschinen) + Matching + Mengen-Heuristik.
- **Ergebnis:** Beliebiger Freitext erzeugt eine sinnvolle Maschinenliste.

### Iteration 3 — „Sinnvolles Layout + Prüfung" (echtes M3 + M4)
- M3: Greedy-Grid-Placement, Hallengröße dynamisch.
- M4: Geometrie-Checks + LLM-Experten-Findings + Ampel.
- **Ergebnis:** Maschinen liegen geordnet, Validierungs-Ampel im UI.

### Iteration 4 — „Live-Chat-Änderungen" (`/api/modify`)
- Orchestrator klassifiziert Instruktionen, führt Teil-Reruns aus.
- Szene aktualisiert sich in Blender, Screenshot refresht.
- **Ergebnis:** „Füge eine zweite Fräse hinzu" verändert die 3D-Fabrik live.

### Iteration 5 — „Politur & Wow" (Demo-Ready)
- Echte Assets für 2–3 Schlüsselmaschinen (Poly Haven Boden/Material, Sketchfab-Maschine), Farb-Codierung nach Status, gesetzte Kamera/Licht.
- Beispiel-Prompts, saubere README mit GIF, Fehlerbehandlung für die Demo.
- **Ergebnis:** Präsentationsreifer, beeindruckender MVP.

> **Puffer-Regel:** Fällt eine Iteration knapp aus, verschiebt sich Politur (It. 5), nie die Lauffähigkeit. Nach jeder Iteration existiert eine vorführbare Version.

---

## 10. Aufteilung auf drei Studierende

**Tag-1-Ritual (alle gemeinsam, ~1–2 h):** Schemas und Mock-JSONs festlegen. Ab dann arbeitet jeder gegen die Mocks — **völlig unabhängig**, Integration erst in Iteration 4/5.

### Person A — „Das Gehirn" (LLM & Orchestrierung)
- **Module:** M1 (Requirements), M2 (Machine Selector), Orchestrator, `llm.py`.
- **Kann sofort loslegen mit:** Nutzertext → `factory.json`. Braucht keine anderen Module.
- **Skills:** Claude API, Prompt-Design, structured output, FastAPI.

### Person B — „Die Logik" (Layout & Validierung)
- **Module:** M3 (Layout), M4 (Validator), `machine_catalog.json`.
- **Kann sofort loslegen mit:** `factory.mock.json` → `layout.json` → `validation.json`. Reine Python-Logik, kein LLM zwingend nötig (Experte kommt später).
- **Skills:** Geometrie/Numpy, Regel-Logik, Testing.

### Person C — „Die Show" (3D & Frontend)
- **Module:** M5 (Scene Builder), `app/streamlit_app.py`, Blender-MCP-Anbindung, Demo & Assets.
- **Kann sofort loslegen mit:** `scene.mock.json` → Blender-Szene + Streamlit-UI, das die Mock-JSONs anzeigt.
- **Skills:** Blender, MCP, Streamlit, UX/Design.

### Integrationspunkte
- **Iteration 1:** gemeinsame Verkabelung der Mocks (halber Abend zu dritt).
- **Iteration 4:** echte Verdrahtung aller Module (zu dritt).
- Dazwischen: asynchron, Kommunikation nur über die Schemas. Vertragstest (`tests/test_contracts.py`) verhindert Drift.

---

## 11. Empfohlener Tech-Stack & Ressourcen (minimale Entwicklungszeit)

### Kern-Bausteine (entscheiden über Erfolg)
| Zweck | Wahl | Warum |
|-------|------|-------|
| LLM | **Anthropic Claude API** (`claude-opus-4-8` für Qualität, `claude-sonnet-5` für Tempo) | Beste structured-output/Tool-Use-Qualität; ein Call ersetzt Parser |
| 3D | **blender-mcp** (bereits im Repo, MCP verbunden) | Claude steuert Blender direkt: Objekte, Materialien, Asset-Download, Viewport-Screenshot — spart Wochen |
| Frontend | **Streamlit** | Chat-UI + Bild-Anzeige in <1 Std.; professioneller Look ohne Frontend-Aufwand |
| Backend | **FastAPI** + Pydantic | Schemas = Pydantic-Modelle „umsonst"; async, wenig Boilerplate |
| Paketmgmt | **uv** oder **poetry** | schnelle, reproduzierbare Umgebung |

### Python-Bibliotheken
- `anthropic` — Claude SDK
- `pydantic` (v2) — Schema-Modelle & Validierung
- `fastapi`, `uvicorn` — Orchestrator
- `streamlit` — UI
- `jsonschema` — Vertragstests
- `numpy` — Geometrie in M3 (optional)
- `mcp` / vorhandener blender-mcp-Client — Blender-Steuerung

### Blender-Assets & 3D-Ressourcen (alle über blender-mcp abrufbar)
- **Primitive** (Iteration 1–4): skalierte Cubes — kostenlos, sofort, ausreichend.
- **Poly Haven** (CC0): Boden-/Wand-Texturen, HDRI-Beleuchtung → sofort „professioneller" Look. Direkt im MCP integriert.
- **Sketchfab** (Suche im MCP): 2–3 echte Maschinenmodelle (CNC, Roboterarm, Förderband) für die Wow-Momente.
- **Hyper3D Rodin / Hunyuan3D** (im MCP): generierte Modelle als Bonus — nur wenn Zeit bleibt.

### Datensätze
- **Kein externer Datensatz nötig.** `data/machine_catalog.json` (~15 Einträge, handkuratiert) ersetzt jede Maschinen-DB. Bewusste Scope-Entscheidung.

### Fertige Referenz
- Das ISW-Paper liefert die konzeptionelle Blaupause (Pipeline + „synthetic expert"). Wir zitieren es und positionieren uns als Metaverse-Erweiterung.

---

## 12. Live-Demo (Drehbuch)

> **Dauer:** ~5 Minuten. **Setup:** Blender offen (MCP läuft), Streamlit-Chat auf dem Beamer, Blender-Viewport zweites Fenster. Backup: aufgezeichnetes GIF/Video, falls Live-LLM hakt.

### Szene 1 — Der leere Start (0:00–0:30)
- **Nutzer tippt:** *„Wir wollen jährlich 50.000 Aluminium-Gehäuse herstellen. Die müssen gefräst, entgratet und lackiert werden."*
- **Was passiert:** Streamlit schickt Text an `/api/generate`. Spinner „Analysiere Anforderungen…".
- **Publikum sieht:** Chat-Nachricht + leere Blender-Halle im zweiten Fenster.

### Szene 2 — Die KI denkt (0:30–1:30)
- **Was passiert:** M1 extrahiert `factory.json`, M2 wählt Maschinen (2× CNC-Fräse, 1× Entgratstation, 1× Lackierkabine).
- **Publikum sieht:** Rechts erscheint eine saubere Tabelle: erkannte Prozessschritte + gewählte Maschinen + Anzahl. „Die KI hat aus einem Satz eine Maschinenliste gemacht."

### Szene 3 — Die Fabrik entsteht (1:30–2:30)
- **Was passiert:** M3 platziert, M4 validiert, M5 baut die Blender-Szene über MCP.
- **Publikum sieht (der Wow-Moment):** In Blender erscheinen **live** Halle, Boden-Textur und farbige Maschinen entlang der Prozesslinie. Kamera schwenkt über die Fabrik.

### Szene 4 — Der KI-Experte warnt (2:30–3:15)
- **Was passiert:** `validation.json` wird angezeigt.
- **Publikum sieht:** Ampel auf **Gelb** + Finding: *„Nach dem Lackieren fehlt üblicherweise ein Trockenofen."* — „Ein KI-Experte prüft das Layout wie ein Kollege."

### Szene 5 — Live-Änderung per Chat (3:15–4:15)
- **Nutzer tippt:** *„Du hast recht — füge einen Trockenofen nach dem Lackieren hinzu und mach die Halle etwas breiter."*
- **Was passiert:** `/api/modify`, Teil-Rerun M2→M5.
- **Publikum sieht:** In Blender erscheint **live** ein neuer Ofen, die Halle wächst, Ampel springt auf **Grün**. „Die Fabrik ist per Sprache editierbar."

### Szene 6 — Der Metaverse-Blick (4:15–5:00)
- **Was passiert:** Wir navigieren frei durch die begehbare 3D-Szene in Blender.
- **Publikum sieht:** Kamerafahrt durch die fertige Fabrik. Abschluss-Satz: *„Von einem Satz zur begehbaren, validierten Fabrik im Open Engineering Metaverse — in unter einer Minute."*

**Zwei vorbereitete Beispiel-Prompts** (in `data/examples/`) als Fallback, falls Live-Eingabe scheitert.

---

## 13. Präsentation (10 Slides)

| # | Titel | Inhalt | Grafik | Sprechertext |
|---|-------|--------|--------|--------------|
| 1 | **AI Engineering Assistant** | Projektname, Team, Modul, Tagline „Cursor für Fabrikplanung" | Hero-Screenshot der 3D-Fabrik | „Was, wenn man eine Fabrik einfach beschreiben könnte — und sie steht?" |
| 2 | **Das Problem** | Erste Simulationsmodelle kosten Wochen manueller Arbeit; Fehler spät = teuer | Kosten-über-Zeit-Kurve (aus Paper) | „Frühe Fehler früh finden spart Kosten — aber die ersten Modelle zu bauen ist langsam und manuell." |
| 3 | **Unsere Idee** | NL-Anforderungen → automatische, validierte 3D-Fabrik; Erweiterung des ISW-Konzepts ins Metaverse | Die Pipeline (Abschnitt 1) | „Wir automatisieren den Weg vom Kundensatz zur begehbaren Fabrik." |
| 4 | **Wissenschaftliche Basis** | Bezug zum ISW-Paper (requirements-driven layout + synthetic expert); unsere Erweiterung: Chat + Metaverse | Paper-Titel + Pfeil „+ Interaktion + 3D" | „Wir bauen auf Forschung der Uni Stuttgart auf und erweitern sie um Interaktivität." |
| 5 | **Systemarchitektur** | 5 Module, JSON-Verträge, Claude + Blender-MCP | Architekturdiagramm (Abschnitt 3.1) | „Fünf entkoppelte Module, die nur über JSON reden — deshalb konnten wir zu dritt parallel bauen." |
| 6 | **Wie die KI denkt** | M1/M2: Freitext → Prozesse → Maschinen (structured output) | Vorher/Nachher: Satz → JSON-Tabelle | „Ein einziger LLM-Aufruf verwandelt Umgangssprache in eine strukturierte Maschinenliste." |
| 7 | **Layout & KI-Experte** | M3 Greedy-Placement, M4 Regeln + synthetischer Experte + Ampel | Layout-Skizze + Ampel/Findings | „Ein zweites KI-Modell prüft das Ergebnis wie ein erfahrener Planer." |
| 8 | **3D im Metaverse** | M5: Blender via MCP, Poly-Haven/Sketchfab-Assets, live editierbar | Screenshot der Blender-Szene | „Über den Blender-MCP steuert die KI die 3D-Szene direkt — inklusive echter Assets." |
| 9 | **Live-Demo** | Übergang zur Vorführung (Drehbuch Abschnitt 12) | Standbild / QR zum Demo-Video | „Genug Folien — schauen wir es uns live an." |
| 10 | **Ausblick & Team** | Future Work: VR-Begehung, echte Simulation, Maschinen-DB; Rollen der 3 Team-Mitglieder; Danke | Roadmap-Pfeil + Team-Fotos | „Der MVP steht. Als Nächstes: VR-Begehung und echte Materialfluss-Simulation. Fragen?" |

---

## Anhang A — Sofort-Checkliste für Tag 1 (zu dritt)

- [ ] GitHub-Repo mit Struktur aus Abschnitt 4 anlegen.
- [ ] Die **4 Schemas** in `schemas/` final festlegen (gemeinsam!).
- [ ] Die **4 Mock-JSONs** in `mocks/` schreiben (ein realistisches Beispiel).
- [ ] `machine_catalog.json` mit ~15 Maschinen skizzieren.
- [ ] `.env.example` + Claude-API-Key besorgen, Blender-MCP-Verbindung testen.
- [ ] Rollen A/B/C bestätigen, Iteration-1-Termin setzen.

**Merksatz des Projekts:** *Ein Satz rein, eine Fabrik raus. Alles andere ist Politur.*
