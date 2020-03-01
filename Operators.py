import logging

from bpy.props import (BoolProperty, FloatProperty, StringProperty)

import bpy
from bpy_extras.io_utils import (axis_conversion, ExportHelper, path_reference_mode, orientation_helper)
from . import Exporter

log = logging.getLogger(__name__)


@orientation_helper(axis_forward='-Z', axis_up='Y')
class ExportOperator(bpy.types.Operator, ExportHelper):
    """Export to a Cocos2d-x text file"""

    bl_idname = 'export_scene.cocos2dx'
    bl_label = 'Export Cocos2d-x'
    bl_options = {'PRESET'}

    filename_ext = '.c3t'
    filter_glob = StringProperty(default='*.c3t', options={'HIDDEN'})

    # context group
    use_selection = BoolProperty(name="Selection Only", description="Export selected objects only", default=False)

    # data group
    export_normals = BoolProperty(name="Export Normals", description="Export one normal per face per per vertex, to represent flat faces and sharp edges", default=True)

    export_uv_maps = BoolProperty(name="Export UVs", description="Exports the UV coordinates and the assigned textures", default=True)

    # object group
    use_mesh_modifiers = BoolProperty(name="Apply Modifiers", description="Apply modifiers", default=True)

    use_mesh_modifiers_render = BoolProperty(name="Use Modifiers Render Settings", description="Use render settings when applying modifiers to mesh objects", default=False)

    global_scale = FloatProperty(name="Scale", min=0.01, max=1000.0, description="Scaling factor applied to all exported objects", default=1.0)

    path_mode = path_reference_mode

    check_extension = True

    def execute(self, context, *args, **kwargs):
        from mathutils import Matrix

        keywords = self.as_keywords(ignore=(
            'axis_forward',  # from IOCocos2dxOrientationHelper
            'axis_up',  # from IOCocos2dxOrientationHelper
            'check_existing',  # from ExportHelper
            # 'filepath',  # from ExportHelper
            'filter_glob',
            'global_scale',
            'path_mode'
        ))

        if 'filepath' in keywords:
            self.filepath = keywords['filepath']
            del keywords['filepath']

        # Create a matrix which incorporates the global scale and the rotation to match Cocos2d-x's coordinate frame.
        global_matrix_conversion = axis_conversion(to_forward=self.axis_forward, to_up=self.axis_up)
        global_matrix = Matrix.Scale(self.global_scale, 4) @ global_matrix_conversion.to_4x4()
        keywords['global_matrix'] = global_matrix

        exporter = Exporter.Exporter(
            context=context,
            source_filepath=bpy.data.filepath,
            dest_filepath=self.filepath,
            path_mode=self.path_mode)

        try:
            exporter.run(context, **keywords)
        except Exception:
            log.exception('export error')

        return {'FINISHED'}
