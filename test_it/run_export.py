import json
import logging
import os

from jsondiff import diff

import bpy

log = logging.getLogger('run_export')
bpy.ops.debug.connect_debugger_pycharm()

source_folder = os.path.dirname(bpy.data.filepath)
source_file = os.path.basename(bpy.data.filepath)

target_folder = os.path.join(os.path.dirname(__file__), '../build/test_it', source_file)
target_file = os.path.join(target_folder, 'scene.json')
log.info('writing to target %s', target_file)
os.makedirs(target_folder, exist_ok=True)

bpy.ops.export_scene.cocos2dx('EXEC_DEFAULT', filepath=target_file, path_mode='RELATIVE')

with open(os.path.join(source_folder, '%s.c3t' % source_file)) as expected_file:
    expected_json = json.load(expected_file)

with open(target_file) as actual_file:
    actual_json = json.load(actual_file)

difference = diff(expected_json, actual_json)

if difference:
    log.error(difference)
    raise EnvironmentError('JSON difference')

log.info('Success!')
