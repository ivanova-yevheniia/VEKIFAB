# VEKIFAB – KI Fabrikplaner

Zuordnung zur Aufgabenstellung – Szenario **„KI Fabrikplaner"**

---

## Kap. 1: Kontext

| #   | WP                   | Beschreibung                                                                          | Tools                                            | Deliverable |
| --- | -------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------ | ----------- |
| A   | AI-Avatar            | Foto → World Labs / Meshy → GLB-Export. Werker/Ingenieur, der die Requirements stellt | readyplayer.me                                   | D1          |
| B   | Claude → Blender     | Claude MCP → Blender Python oder meshy.ai zur Erstellung von Werkzeugmaschinen        | Blender, Claude Desktop (siehe Aufgabenstellung) | D1          |
| C   | Image to Physics     | Erstellung der Fertigungshalle aus Bildmaterial                                       | image-blaster                                    | D1          |
| D   | Pipeline / Szene     | Kombination und Animation von A, B und C als Serious Game                             | Unity                                            | D2          |
| E   | Prozessdokumentation | Dokumentation des Ablaufs als PowerPoint                                              | Copilot / Claude                                 | D3          |

---

## Kap. 2: Fallzuordnung

- **Fall 3**, sofern mindestens 1 Roboter verwendet wird (übrige Elemente sind einfache Werkzeugmaschinen)
- **Git Repo:** `VEKIFAB`

---

## Szenenbeschreibung (Demo in Unity / Serious Game)

1. Der Ingenieur (Mensch) beschreibt technische Details – z. B. die verfügbare Fertigungsfläche – und gibt diese an einem PC ein. Anschließend sendet er die Eingabe ab.
2. Claude MCP–Blender bzw. meshy.ai generiert anhand der eingegebenen Parameter Werkzeugmaschinen/Roboter.
3. Claude generiert mithilfe von image-blaster die passende Fertigungshalle.
4. Der Ingenieur kann mit seinem Avatar durch die erstellte Fabrikhalle laufen.

> Alles wird im Voraus erstellt/vorbereitet. Das Serious Game ist das Ergebnis eines Runs (der Avatar bewegt sich durch die zuvor erstellte Fabrikhalle).

---

## Arbeitspakete

| ToDo | Verantwortlich | Zugehöriges WP | Konkrete Aufgabe                                                                                                                             |
| ---- | -------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Jenny          | B              | Werkzeugmaschinen mit Claude in Blender (requirements.json ergänzen)                                                                         |
| 2    | Yannic         | C              | Fertigungshalle (leer) mit image-blast und Claude (requirements.json ergänzen), Gaussian Splat in Unreal Engin Laden und Projekt exportieren |
| 3    | Chris          | A              | Beliebigen Avatar erstellen (Tools aus Aufgabenstellung)                                                                                     |
| 4    | Y, **J**, C    | D              | UnrealEngine-Szenario erstellen                                                                                                              |
| 5    | Y, J, C        | E              | Plain White jeder macht seine Folien wo er sein WP beschreibt                                                                                |
| 6    | C              | E              | CoPilot einheitliche umformatierung                                                                                                          |
| 7    | Y, J, C        | D              | Unreal Projekt als exe Exportieren                                                                               |


