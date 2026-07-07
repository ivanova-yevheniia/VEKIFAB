"""
export_all_glb.py — Re-export a .glb from every actual station .blend.

Opens each station .blend in exports/blend/ and writes exports/glb/<name>.glb
with the WP B export settings (GLB, Y-up for Unity, modifiers applied, custom
properties as glTF extras). The .glb is generated straight from the model on
disk, so it matches the actual Blender file exactly.

Run headless:
    blender --background --python export_all_glb.py
"""

import os
import glob

import bpy

_HERE = os.path.dirname(os.path.abspath(__file__))
_B_ROOT = os.path.dirname(_HERE)
_BLEND_DIR = os.path.join(_B_ROOT, "exports", "blend")
_GLB_DIR = os.path.join(_B_ROOT, "exports", "glb")

# Station .blend files (exclude the utils smoke test — it is not a station).
_SKIP = {"utils_smoke_test"}


def _station_blends():
    out = []
    for path in sorted(glob.glob(os.path.join(_BLEND_DIR, "*.blend"))):
        name = os.path.splitext(os.path.basename(path))[0]
        if name in _SKIP:
            continue
        out.append((name, path))
    return out


def export_one(name, blend_path):
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    os.makedirs(_GLB_DIR, exist_ok=True)
    glb_path = os.path.join(_GLB_DIR, name + ".glb")
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format="GLB",
        export_yup=True,       # Y-up for Unity
        export_apply=True,     # apply modifiers (bevel, etc.)
        export_extras=True,    # custom properties -> glTF extras
        use_selection=False,
    )
    size_kb = os.path.getsize(glb_path) // 1024 if os.path.exists(glb_path) else 0
    print("[glb] %-22s -> %s (%d KB, %d objects)"
          % (name, os.path.basename(glb_path), size_kb, len(bpy.data.objects)))


def main():
    stations = _station_blends()
    if not stations:
        print("[glb] no station .blend files found in", _BLEND_DIR)
        return
    for name, path in stations:
        export_one(name, path)
    print("[glb] done:", len(stations), "station(s)")


if __name__ == "__main__":
    main()
