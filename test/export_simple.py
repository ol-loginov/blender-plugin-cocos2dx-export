import bpy
import tempfile

target = tempfile.NamedTemporaryFile(suffix='.json')
print('writing to target %s' % target.name)

bpy.ops.debug.connect_debugger_pycharm()
bpy.ops.export_scene.cocos2dx(filepath=target.name)
