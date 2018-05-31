import bpy
from bpy import context
import os

print ("Initializing exporting of obj models...")

export_directory = os.path.abspath(__file__+'/../../export/obj')+'/'
scene_objects = bpy.context.scene.objects
print (scene_objects)

bpy.context.scene.layers[19] = True

print ("Deselecting all scene objects")
bpy.ops.object.select_all(action='DESELECT')

print ("Selectable objects are:")
print (bpy.context.selectable_objects)

for obj in scene_objects:
    name = obj.name
    if not name.endswith("w"):
        print ("Object name is:",name)
        print("Selecting the object..")
        obj.select = True
        print ("Exporting the object...")
        bpy.ops.export_scene.obj(filepath=export_directory+name+'.obj', use_selection=True, axis_forward='-Z', axis_up='Y')
        print ("Deselecting the object")
        obj.select = False

print ("Done.\n")