"""
generate_full_factory.py — VEKIFAB WP B orchestrator.

Placeholder. Assembles the complete production line by reading
requirements/factory_description.json and dispatching each station entry to the
matching generate_*.py generator, then exports .blend / .glb.

No geometry is generated yet. Planned flow:

  1. Load requirements/factory_description.json.
  2. For each station, call the matching generator (by 'type').
  3. Build conveyors (CONVEYOR_*) connecting the stations.
  4. Add colliders / triggers for the Unity avatar walkthrough.
  5. Export to exports/blend/ and exports/glb/, save screenshots.

See docs/workflow.md and docs/unity_import_notes.md.
"""

# import common_blender_utils as utils
# import generate_loading_station
# import generate_assembly_station
# import generate_robot_cell
# import generate_vision_station
# import generate_functional_test
# import generate_packaging_station
# import generate_storage_area


def build_factory(description_path: str):
    """Build the full factory from a factory_description.json. Placeholder."""
    raise NotImplementedError


if __name__ == "__main__":
    print("generate_full_factory.py — placeholder, no geometry generated yet.")
