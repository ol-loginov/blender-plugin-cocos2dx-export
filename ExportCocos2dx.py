from os.path import dirname

from mathutils import Matrix


class Exporter:
    def __init__(self, context, source_filepath, dest_filepath, path_mode):
        self.context = context

        self.dest_filepath = dest_filepath

        # Texture images etc. can use paths relative to the source file. These paths have to be resolved.
        self._source_directory = dirname(source_filepath)
        self._dest_directory = dirname(dest_filepath)
        self._path_mode = path_mode
        self._copy_set = set()  # A set of images which need to be copied. TODO

        self._use_cycles = context.scene.render.engine == 'CYCLES'
        self._exported_materials_to_id_map = {}

        self.version = '0.7'
        self.id = ''
        self.meshes = []
        self.materials = []
        self.nodes = []

    def run(self, context,
            *,
            global_matrix=None,
            use_selection=False,
            export_normals=False,
            export_uv_maps=False,
            export_animations_only=False,
            use_mesh_modifiers=False,
            use_mesh_modifiers_render=False):
        """Exports a scene in the Cocos2d-x format.
         :param global_matrix: The matrix applied to the transform of the nodes. Useful for rotating the coordinate frame
             and applying a global scale.
         """

        # Life is much easier if there is always a global matrix. Fall back to the identity matrix.
        if global_matrix is None:
            global_matrix = Matrix()
