import bpy
from bpy import context
import csv
from csv import DictReader
import math
from mathutils import Matrix
import os
import time


### PHASE 1 - Recreate the block

scene = bpy.context.scene

# Find the latest file
save_files = [f for f in os.listdir(os.path.abspath(__file__+'/../../save')) if 'csv' in f]
number_of_files = len(save_files)
selected_file = number_of_files - 1

CSVFile = os.path.abspath(__file__+'/../../save') + '/' + str(save_files[selected_file])
DataFile = CSVFile ### The CSVfile is the file that holds the instructions
# Count the rows
with open(DataFile,"r") as D:
    CSVreader = csv.reader(D,delimiter = ",")
    data = list(CSVreader)
    row_count = (len(data)-1)
    
# Retrieve the data from the csv file and seperate them to item name, x location, y location, z location and rotation
with open(DataFile) as D:
    items = [row["ITEM"] for row in DictReader(D)]
with open(DataFile) as X:
    locationX = [row["X"] for row in DictReader(X)]
with open(DataFile) as Y:
    locationY = [row["Y"] for row in DictReader(Y)]
with open(DataFile) as Z:
    locationZ = [row["Z"] for row in DictReader(Z)]
with open(DataFile) as R:
    rotationR = [row["ROTATION"] for row in DictReader(R)]

i=0 ### Start from the first row
while i<row_count:
    
    x = float(locationX[i])
    y = float(locationY[i])
    z = float(locationZ[i])
    r = float(rotationR[i])
    
    src_obj = bpy.data.objects[items[i]]
    new_obj = src_obj.copy()
    new_obj.data = src_obj.data.copy()
    new_obj.animation_data_clear()
    scene.objects.link(new_obj)
    
    new_obj.location[0] = x
    new_obj.location[1] = y
    new_obj.location[2] = z
    new_obj.rotation_euler = (Matrix.Rotation(r, 3, 'Z') * new_obj.rotation_euler.to_matrix()).to_euler()

    i = i+1


### PHASE 2 - Delete all the unused blocks

bpy.context.scene.layers[19] = True
for obj in scene.objects:
    if obj.location[0] >= 50:
        bpy.data.objects[obj.name].select = True
        bpy.ops.object.delete()

bpy.context.scene.layers[18] = True
for obj in scene.objects:
    if obj.location[0] <= -50:
        bpy.data.objects[obj.name].select = True
        bpy.ops.object.delete()


### PHASE 3 - Export the STL file

export_directory = os.path.abspath(__file__+'/../../export/stl')+'/'
scene_objects = bpy.context.scene.objects

bpy.context.scene.layers[0] = True

bpy.ops.object.select_all(action='DESELECT')

date = time.strftime("%Y%m%d%H%M%S")
bpy.ops.export_mesh.stl(filepath=export_directory+'3DPRINT_'+date+'_STL.stl', axis_forward='Y', axis_up='Z')

print ("Done.\n")