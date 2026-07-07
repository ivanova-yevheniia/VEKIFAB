"""
material_engine.py — Generic material creation / reuse.

Given a material name (a key into the parameter file's `material_library`),
create the Blender material once and reuse it thereafter. Materials are never
duplicated: the engine caches by name and also reuses any existing
`bpy.data.materials` entry with the same name.

Material definitions (PBR values + optional emission) come entirely from the
JSON `material_library`; this module holds no colours of its own.
"""

try:
    import bpy
    _HAS_BPY = True
except ImportError:
    bpy = None
    _HAS_BPY = False


class MaterialEngine:
    def __init__(self, material_library=None):
        self.library = material_library or {}
        self._cache = {}
        self.warnings = []

    def _principled(self, mat):
        node = mat.node_tree.nodes.get("Principled BSDF")
        if node is None:
            for n in mat.node_tree.nodes:
                if n.type == "BSDF_PRINCIPLED":
                    return n
        return node

    def _apply(self, mat, defn):
        mat.use_nodes = True
        bsdf = self._principled(mat)
        if bsdf is None:
            return
        color = defn.get("base_color", [0.8, 0.8, 0.8, 1.0])
        if len(color) == 3:
            color = list(color) + [1.0]
        bsdf.inputs["Base Color"].default_value = color
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = float(defn.get("metallic", 0.0))
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = float(defn.get("roughness", 0.5))
        alpha = float(defn.get("alpha", color[3] if len(color) == 4 else 1.0))
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        if alpha < 1.0:
            try:
                mat.blend_method = "BLEND"
            except (AttributeError, TypeError):
                pass
        strength = float(defn.get("emission_strength", 0.0))
        if strength > 0.0:
            ecol = defn.get("emission_color", color)
            if len(ecol) == 3:
                ecol = list(ecol) + [1.0]
            for key in ("Emission Color", "Emission"):
                if key in bsdf.inputs:
                    bsdf.inputs[key].default_value = ecol
                    break
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = strength
        mat.diffuse_color = color

    def get(self, name):
        """Return the material for `name`, creating it once and reusing after."""
        if not _HAS_BPY or not name:
            return None
        if name in self._cache:
            return self._cache[name]
        # Reuse an existing data-block of the same name if present.
        mat = bpy.data.materials.get(name)
        if mat is None:
            mat = bpy.data.materials.new(name)
            defn = self.library.get(name)
            if defn is None:
                self.warnings.append("material '%s' not in library; using default" % name)
                defn = {}
            self._apply(mat, defn)
        self._cache[name] = mat
        return mat

    def build_all(self):
        """Pre-create every material in the library (optional warm-up)."""
        for name in self.library:
            self.get(name)
        return dict(self._cache)
