import bge
import csv
import time
from config import *

scene = bge.logic.getCurrentScene


def save_function(file):
    """Export the model's objects (name,location) to a csv file."""
    print("Saving the data to the external file...")
    # Get the list of scenes
    scenes = bge.logic.getSceneList()
    
    # The file to save the values. Needs to be opened first.
    list_file = data_dir + file
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
            excluded_objects = ['lamp', 'sun', 'camera', 'preview', 'placeholder', 'ground', 'grid', 'background', 'empty', 'origin', 'selected']
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
   
def save_bathroom():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    
    if mouse_over.positive and left_click.positive:
        save_function("bathroom"+date+".csv")
        
def save_bedroom():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    
    if mouse_over.positive and left_click.positive:
        save_function("bedroom"+date+".csv")

def save_kitchen():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    
    if mouse_over.positive and left_click.positive:
        save_function("kitchen"+date+".csv")
        
def save_livingroom():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    
    if mouse_over.positive and left_click.positive:
        save_function("/livingroom/livingroom"+date+".csv")
