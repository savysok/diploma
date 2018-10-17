import bge
import csv                      ### csv - The CSV Library for parsing the csv file
from csv import DictReader      ### DictReader - DictReader is needed to read the csv file's columns
import math
import random
import time
from config import *


def save_function(file):
    """Export the model's objects (name,location) to a csv file."""
    print("Saving the data to the external file...")
    # Get the list of scenes
    scenes = bge.logic.getSceneList()
    
    # The file to save the values. Needs to be opened first.
    list_file = save_dir + file
    list_file_open = open(list_file, 'w')
    #print("Opening list_file at", list_file)
    
    

    # Iterate through the MAIN scene's objects
    for scene in scenes :
        if scene.name == "MAIN":
            #print("scene : %s"%scene.name)
            # List of all the objects in the game
            object_list = [obj for obj in scene.objects]
            #print(object_list)
            # Iterate through the objects and find it's values for
            # name, x position, y position and z position
            excluded_objects = ['lamp', 'sun', 'camera', 'preview', 'placeholder', 'ground', 'grid', 'background', 'empty', 'origin', 'selected', 'button']
            list_file_open.write("ITEM,X,Y,Z,ROTATION\n")
            for obj in object_list:
                name = str(obj.name) ### Strings are needed to be able to write in the txt file
                x = str(round(obj.worldPosition[0], 2))
                y = str(round(obj.worldPosition[1], 2))
                z = str(round(obj.worldPosition[2], 2))
                r = str(round(obj.localOrientation.to_euler().z, 3))
                #print(name, "'s rotation is:", r)

                # Write the values to the file
                #print("Saving", name, "at", x, y, z, "to the file.")
                # Save only the objects that don't have a name that
                # begins with the 'excluded_objects' list
                # (the default scene items like the camera, the lights etc)
                if not any(excluded_objects in name for excluded_objects in excluded_objects):
                    list_file_open.write(name+","+x+","+y+","+z+","+r+"\n")
                    #print(name)

    list_file_open.close()
    print("Data exported. Closing the open list file.")
    print("Done.\n")
   
   
date = time.strftime("%Y%m%d%H%M%S")
   
def save_block():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    
    if mouse_over.positive and left_click.positive:
        save_function("block"+date+".csv")



def clear_workspace():
    
    object_types = ('wall', 'floor', 'window', 'door', 'stair', 'furniture', 'appliance')
    
    scene_list = bge.logic.getSceneList()
    
    for scene in scene_list:
        if scene.name == "MAIN":
            for object in scene.objects:
                if any(object_types in object.name for object_types in object_types) and object.worldPosition.x >= -50:
                    object.endObject()


### OLD

### CREATE_BUILDING - Function to create a building with instructions from a CSV file
def recreate_block(CSVfile):
    
    controller = bge.logic.getCurrentController()
    #print ("Controller is:",controller)
    own = controller.owner
    #print ("Owner is:",own)
    
    scene_list = bge.logic.getSceneList()
    
    for scene in scene_list:
        if scene.name == "MAIN":
            
            ghost = scene.objects["preview.block_preview"] # The building editor preview
    
            ### First, delete all the grid objects.
            #clear_grid()
            
            DataFile = CSVfile ### The CSVfile is the file that holds the instructions
            ### Count the rows
            with open(DataFile,"r") as D:
                CSVreader = csv.reader(D,delimiter = ",")
                data = list(CSVreader)
                row_count = (len(data)-1)
                #print ("There are ",row_count,"rows of data")
            
            ### Retrieve the data from the csv file and seperate them to item name, x location, y location, z location and rotation
            with open(DataFile) as D:
                items = [row["ITEM"] for row in DictReader(D)]
                #print (items)
            with open(DataFile) as X:
                locationX = [row["X"] for row in DictReader(X)]
                #print (locationX)
            with open(DataFile) as Y:
                locationY = [row["Y"] for row in DictReader(Y)]
                #print (locationY)
            with open(DataFile) as Z:
                locationZ = [row["Z"] for row in DictReader(Z)]
                #print (locationZ)
            with open(DataFile) as R:
                rotationR = [row["ROTATION"] for row in DictReader(R)]
                #print (rotationR)
            #with open(DataFile) as I:
            #    id_num = [row["ID"] for row in DictReader(R)]
            #    #print (id_num)
                
            i=0 ### Start from the first row
            while i<=row_count:
                #print ("i is:",i)
                #print ("Item is:",items[i]) ### This is used later
                #print ("X position is:",locationX[i])
                x = float(locationX[i])
                #print ("Y position is:",locationY[i])
                y = float(locationY[i])
                #print ("Z position is:",locationZ[i])
                z = float(locationZ[i])
                #print ("Rotation is:",rotationR[i])
                r = float(rotationR[i])
                #print (r)
                ghost.worldPosition = [x,y,z]
                #print(ghost.worldOrientation.to_euler().z)
                
                ### This one was tricky: rotate the empty according to the radian(?) values of the CSV file
                ### First, convert the local orientation to Euler
                xyz = ghost.localOrientation.to_euler()
                #print ("Before the rotation. Z rotation is:",xyz[2])
                ### Then, change the Z value of the rotation to the one from the CSV file
                xyz[2] = r
                #print ("After the rotation. Z rotation is:",xyz[2])
                ### Finally, change the empty's local orientation with the new Z value
                ghost.localOrientation = xyz.to_matrix()
                
                obj = scene.addObject(items[i], ghost, 0)
                obj["ID"] = random.randint(100000,999999) # give a unique ID number
                #obj["ID"] = id_num
                i = i+1


save_files = [f for f in os.listdir(save_dir) if 'csv' in f]
number_of_files = len(save_files)
selected_file = number_of_files - 1


def load_block():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    mouse_over = controller.sensors["mouse_over"]
    right_click = controller.sensors["right_click"]
    
    global selected_file
    
    if mouse_over.positive and right_click.positive and selected_file <= 0:
        selected_file = number_of_files - 1
        print (selected_file)
    
    if mouse_over.positive and right_click.positive and selected_file > 0:
        
        print ("Loading the data from the external file...")
        
        clear_workspace()
        
        recreate_block(save_dir+'/'+save_files[selected_file])
        
        selected_file -= 1
        
        print ("Done.\n")