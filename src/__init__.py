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

import importlib

import bpy
from . import Operators

importlib.reload(Operators)


def menu_func_export(self, context):
    self.layout.operator(Operators.ExportOperator.bl_idname, text='Cocos2d-x (.c3t)')


def register():
    bpy.utils.register_class(Operators.ExportOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(Operators.ExportOperator)


if __name__ == '__main__':
    register()
