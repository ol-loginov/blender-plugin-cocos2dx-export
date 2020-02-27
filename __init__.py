#!/usr/bin/env python

bl_info = {
    "name": "Cocos2d-x exporter",
    "author": "ol-loginov@gmail.com",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "File > Export",
    "description": "Exports objects to Cocos2d-x",
    "category": "Import-Export"
}

if "bpy" in locals():
    import importlib

    importlib.reload('ExportCocos2dxCommand')
else:
    from . import ExportCocos2dxCommand

import bpy


def menu_func_export(self, context):
    self.layout.operator(ExportCocos2dxCommand.Command.bl_idname, text='Cocos2d-x (.c3t)')


def register():
    bpy.utils.register_class(ExportCocos2dxCommand.Command)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.INFO_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportCocos2dxCommand.Command)


if __name__ == '__main__':
    register()
