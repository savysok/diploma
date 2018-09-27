import bge
import math
import random
from grid import generate_grid
from block import create_object_list, move_block_to_preview, create_initial_block, place_block


# DEBUGGING
DEBUG=False
#print("(Debugging is set to", DEBUG, ")\n")
def debug_print(*args):
    """Function that set the debugging mode On (True) or Off (False)"""
    if DEBUG:
        print(*args)


scene = bge.logic.getCurrentScene() # The current scene (MAIN)

preview_part = scene.objects["preview.parts_preview"] # The part preview object (Suzanne)
preview_space = scene.objects["preview.parts_space"] # The space preview object
preview_block = scene.objects["preview.block_preview"] # The building editor preview


generate_grid(0) # Generate the grid(s) at level 0


# The objects sets
set001 = [
    
    ('wall.corner.000', 'wall.000', 'wall.001',
    'wall.003', 'column.001', 'wall.seperator.single.solid.001', 
    'wall.seperator.single.door.001', 'wall.seperator.corner.solid.001',
    'wall.seperator.corner.solid.002', 'wall.seperator.corner.solid.003'),
    
    ('floor.01.000', 'floor.01.001', 'floor.01.002', 'floor.01.003', 'floor.01.004',
    'floor.02.000', 'floor.02.001', 'floor.02.002', 'floor.02.003', 'floor.02.004'), 
    
    ('door.001', 'door.000', 'window.000', 'window.001', 'door.interior.000')
    ]

set002 = [
    
    ('wall.corner.001', 'wall.000', 'wall.001',
    'wall.003', 'column.001', 'wall.seperator.single.solid.001', 
    'wall.seperator.single.door.001', 'wall.seperator.corner.solid.001',
    'wall.seperator.corner.solid.002', 'wall.seperator.corner.solid.003'),
    
    ('floor.01.000', 'floor.01.001', 'floor.01.002', 'floor.01.003', 'floor.01.004',
    'floor.02.000', 'floor.02.001', 'floor.02.002', 'floor.02.003', 'floor.02.004'), 
    
    ('door.001', 'door.000', 'window.000', 'window.001', 'door.interior.000')
    ]
    
set003 = [
    
    ('wall.corner.002', 'wall.002', 'wall.001',
    'wall.003', 'column.001', 'wall.seperator.single.solid.001', 
    'wall.seperator.single.door.001', 'wall.seperator.corner.solid.001',
    'wall.seperator.corner.solid.002', 'wall.seperator.corner.solid.003'),
    
    ('floor.01.000', 'floor.01.001', 'floor.01.002', 'floor.01.003', 'floor.01.004',
    'floor.02.000', 'floor.02.001', 'floor.02.002', 'floor.02.003', 'floor.02.004'), 
    
    ('door.001', 'door.000', 'window.000', 'window.001', 'door.interior.000')
    ]

selected_part = set001[0][0] # The first selected part


previous_object = scene.objects["ground.block_editor"]


def object():
    """The main function that controls the placement, rotation and deletion
    of the objects in the program.
    """
    
    global previous_object # Declare the previous object as global
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    # Sensors
    mouse_over = controller.sensors["mouse_over"]
    R = controller.sensors["R"] # Rotation
    left_click = controller.sensors["left_click"] # Placement
    right_click = controller.sensors["right_click"] # Deletion
    Lshift = controller.sensors["Lshift"] # Shift+R: mouse over object rotation
    
    if mouse_over.positive:
        
        global rayObj
        rayObj = mouse_over.hitObject # The object that the mouse is pointing
        debug_print("The object hit by the ray is:", rayObj)
        debug_print("Ray object's world position is:", rayObj.worldPosition)
        
        rayPos = mouse_over.hitPosition # The ray's position
        debug_print("The ray's position is: ", rayPos)
        debug_print("The ray's X position is: ", rayPos[0])
        debug_print("The ray's Y position is: ", rayPos[1])
        debug_print("The ray's Z position is: ", rayPos[2])
        debug_print("\n")
        
        if rayObj.worldPosition != previous_object.worldPosition:
            
            #print("The object has changed. New object is:",rayObj,"at",rayObj.worldPosition)
            previous_object = rayObj
        
            obj_type = rayObj["type"] # The object's type
            debug_print("The object type is:", obj_type)
            
            rayNormal = mouse_over.hitNormal # The object's normal face
            debug_print("The object normal is:", rayNormal)
            debug_print(" rayNormal[0] is:", rayNormal[0], "\n", "rayNormal[1] is:", rayNormal[1], "\n", "rayNormal[2] is:", rayNormal[2], "\n",)
            
            debug_print(rayObj.worldPosition)
            debug_print(rayObj.worldOrientation)
            
            length = rayObj["length"]   # The object's length
            width = rayObj["width"]     # The object's width
            height = rayObj["height"]   # The object's height
            
            debug_print("Object's dimensions are:",length, width, height)
            
            #if obj_type != "placeholder" and obj_type != "grid_building" and rayPos[0] < 50.0: # For the block editor
            included_objects = ['grid_block', 'wall', 'floor', 'window']
            #if not any(excluded_objects in name for excluded_objects in excluded_objects):
            #if obj_type == "grid_block" or obj_type == "wall" and rayPos[0] < 50.0: # For the block editor
            if any(included_objects in obj_type for included_objects in included_objects) and rayPos[0] < 50.0:     
                # X axis
                if rayNormal[0] == 1:
                    preview_space.worldPosition = [rayObj.worldPosition.x + length, rayObj.worldPosition.y, rayObj.worldPosition.z]
                if rayNormal[0] == -1:
                    preview_space.worldPosition = [rayObj.worldPosition.x - length, rayObj.worldPosition.y, rayObj.worldPosition.z]
                
                # Y axis
                if rayNormal[1] == 1:
                    preview_space.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y + width, rayObj.worldPosition.z]
                if rayNormal[1] == -1:
                    preview_space.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y - width, rayObj.worldPosition.z]
                    
                # Z axis
                if rayNormal[2] == 1:
                    preview_space.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayObj.worldPosition.z + height]
                    #print(preview_space.worldPosition)
            
            
            if rayPos[0] > 50.0: # For the building editor
                
                # X axis
                if rayNormal[0] == 1:
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayObj.worldPosition.z]
                if rayNormal[0] == -1:
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayObj.worldPosition.z]
                
                # Y axis
                if rayNormal[1] == 1:
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayObj.worldPosition.z]
                if rayNormal[1] == -1:
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y , rayObj.worldPosition.z]
                    
                # Z axis
                if rayNormal[2] == 1:
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayObj.worldPosition.z + height]
                    move_block_to_preview()
                    #print(preview_block.worldPosition)
                    
            
        if R.positive and not Lshift.positive:  # Rotate only the preview object
            own.applyRotation([0,0,math.pi/2])
            
        if R.positive and Lshift.positive:      # Rotate the mouse over object
            rayObj.applyRotation([0,0,-math.pi/2])
        
        included_objects = ['grid_block', 'wall', 'floor', 'window', 'door']        
        if left_click.positive:                 # Place an item on the preview's spot
            if rayPos[0] < 50.0 and rayObj["type"] == "grid_block" or rayObj["type"] == "wall" or rayObj["type"] == "floor":
                obj = scene.addObject(selected_part, preview_space, 0)
                obj.worldPosition = preview_space.worldPosition
                obj.worldOrientation = preview_space.worldOrientation
                obj["ID"] = random.randint(100000,999999) # give a unique ID number
            if rayPos[0] > 50.0:
                #create_object_list("bathroom20180727112525.csv")
                #create_initial_block()
                place_block()
            room_grids = ('grid_block_bathroom', 'grid_block_bedroom', 'grid_block_kitchen', 'grid_block_livingroom')
            #if rayPos[0] < 50 and rayObj["type"] == "grid_block_bathroom":
            if any(room_grids in rayObj["type"] for room_grids in room_grids):
                obj = scene.addObject(selected_part, preview_space, 0)
                obj.worldPosition = preview_space.worldPosition
                obj.worldOrientation = preview_space.worldOrientation
                obj["ID"] = random.randint(100000,999999) # give a unique ID number
                ### add a copy of the item at the building editor
                def add_copy_object(preview_block):
                    obj_copy = scene.addObject(selected_part, preview_space, 0)
                    obj_copy.worldPosition.x = scene.objects[preview_block].worldPosition.x + obj.worldPosition.x + 0.5
                    obj_copy.worldPosition.y = scene.objects[preview_block].worldPosition.y + obj.worldPosition.y + 0.5
                    obj_copy.worldPosition.z = scene.objects[preview_block].worldPosition.z + obj.worldPosition.z
                    obj_copy.worldOrientation = preview_space.worldOrientation
                    obj_copy["ID"] = obj["ID"]
                if rayObj["type"] == "grid_block_bathroom":
                    add_copy_object("preview.block_bathroom")
                if rayObj["type"] == "grid_block_bedroom":
                    add_copy_object("preview.block_bedroom")
                if rayObj["type"] == "grid_block_kitchen":
                    add_copy_object("preview.block_kitchen")
                if rayObj["type"] == "grid_block_livingroom":
                    add_copy_object("preview.block_livingroom")
                    
            
        if right_click.positive:   # Delete object (exclude grid, previews and placeholders)
            if rayObj["type"] == "wall" or rayObj["type"] == "floor" or rayObj["type"] == "window" or rayObj["type"] == "door" or rayObj["type"] == "furniture":
                for object in scene.objects:
                    if object.name == rayObj.name and object["ID"] == rayObj["ID"]:
                        object.endObject()
                    previous_object = scene.objects["ground.block_editor"]
                previous_object = scene.objects["ground.block_editor"]
                






def create_parts_buttons(set_of_items, category, max_items):
    """Function to create the buttons. Replaces the placeholders with the meshes from the object lists."""
    
    ID = 0 # Starting array number
    
    number_of_items = len(set_of_items)
    
    # "{0:0=3d}".format(o) <== This means to format the numbers to 3 decimal one. For example, write 3 as 003
    object_button = ["placeholder."+category+"."+str("{0:0=3d}".format(o)) for o in range(0, number_of_items)]
    
    def clear_previous_buttons(): # Replace all the buttons with their default placeholder
        for i in range(0, max_items):
            object = scene.objects[object_button[i]]
            object.replaceMesh("placeholder.parts.default")
   
    for i in range(0, number_of_items):
        object = scene.objects[object_button[i]]
        object["ID"] = i
        object.replaceMesh(set_of_items[i])
        
create_parts_buttons(set001[0], "wall", 9)
create_parts_buttons(set001[1], "floor", 9)
create_parts_buttons(set001[2], "window", 4)

global selected_set
selected_set = set001

def set_object():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    preview = scene.objects["preview.parts_preview"]
    selected_item = scene.objects["selected_item"]
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    
    if mouse_over.positive and left_click.positive:
        ID = own["ID"]
        #print("Placeholder's ID is:",own["ID"])
        print(own.name)
        global selected_part
        if "wall" in own.name: 
            selected_part = selected_set[0][ID]
        if "floor" in own.name: 
            selected_part = selected_set[1][ID]
        if "window" in own.name: 
            selected_part = selected_set[2][ID]
        selected_item.worldPosition = own.worldPosition
        print(selected_set)


def preview_mesh():
    """Function to change the preview mesh to the currently selected."""

    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    global selected_part
    own.replaceMesh(selected_part)
    
    
current_set = 0

def change_set():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    
    global selected_set
    global current_set
    
    available_sets = (set001, set002, set003)
    
    if mouse_over.positive and left_click.positive:
        print("CURRENT SET:",current_set)
        if current_set == len(available_sets)-1:
            current_set = -1
            selected_set = available_sets[current_set]
        if current_set < len(available_sets)-1:
            current_set += 1
            selected_set = available_sets[current_set]
        
        create_parts_buttons(available_sets[current_set][0], "wall", 9)
        create_parts_buttons(available_sets[current_set][1], "floor", 9)
        create_parts_buttons(available_sets[current_set][2], "window", 4)
        