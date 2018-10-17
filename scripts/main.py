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
    'wall.003', 'column.000', 'wall.seperator.single.solid.001', 
    'wall.seperator.single.door.001', 'wall.seperator.corner.solid.001',
    'wall.seperator.corner.solid.002', 'wall.seperator.corner.solid.003'),
    
    ('floor.01.000', 'floor.01.001', 'floor.01.002', 'floor.01.003', 'floor.01.004',
    'floor.02.000', 'floor.02.001', 'floor.02.002', 'floor.02.003', 'floor.02.004'), 
    
    ('door.001', 'door.000', 'window.000', 'window.001', 'door.interior.000')
    ]

set002 = [
    
    ('wall.corner.001', 'wall.005', 'wall.004',
    'wall.003', 'column.001', 'wall.seperator.single.solid.002', 
    'wall.seperator.single.door.002', 'door.interior.002'),
    
    ('floor.04.000', 'floor.04.001', 'floor.04.002', 'floor.04.003', 'floor.04.004',
    'floor.03.000', 'floor.03.001', 'floor.03.002', 'floor.03.003', 'floor.03.004'), 
    
    ('door.001', 'door.000', 'window.002')
    ]
    
set003 = [
    
    ('wall.corner.002', 'wall.002', 'placeholder.parts.default', 'placeholder.parts.default', 
    'column.002'),
    
    ('floor.05.000', 'floor.05.001', 'floor.05.002', 'floor.05.003', 'floor.05.004',
    'floor.05.005', 'floor.05.006', 'floor.05.007', 'floor.05.008', 'floor.05.009'), 
    
    ('placeholder.parts.default', 'placeholder.parts.default')
    ]
    
set004 = [
    
    ('placeholder.parts.default', 'placeholder.parts.default', 'placeholder.parts.default', 'placeholder.parts.default', 'stairs.001'),
    
    ('placeholder.parts.default', 'placeholder.parts.default'), 
    
    ('placeholder.parts.default', 'placeholder.parts.default')
    ]
    
set005 = [
    
    ('furniture.table.000', 'furniture.chair.000', 'furniture.bench.000',
    'furniture.bench.001', 'furniture.oven.000', 'furniture.fridge.000'),
    
    ('placeholder.parts.default', 'placeholder.parts.default'), 
    
    ('placeholder.parts.default', 'placeholder.parts.default')
    ]
    
set006 = [
    
    ('furniture.bedside.000', 'furniture.bed.000'),
    
    ('placeholder.parts.default', 'placeholder.parts.default'), 
    
    ('placeholder.parts.default', 'placeholder.parts.default')
    ]

selected_part = set001[0][0] # The first selected part


previous_object = scene.objects["ground.block_editor"]

#global creation_mode
#creation_mode = 1

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
    Rshift = controller.sensors["Rshift"] # Shift+R: mouse over object rotation
    Lctrl = controller.sensors["Lctrl"] # CTRL: delete group
    
    if mouse_over.positive:
        
        creation_mode = own["mode"]
        
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
            included_objects = ['grid_block', 'grid_building', 'wall', 'floor', 'window', 'stair', 'furniture', 'appliance']
            #if not any(excluded_objects in name for excluded_objects in excluded_objects):
            #if obj_type == "grid_block" or obj_type == "wall" and rayPos[0] < 50.0: # For the block editor
            #if any(included_objects in obj_type for included_objects in included_objects) and rayPos[0] < 50.0:
            if any(included_objects in obj_type for included_objects in included_objects) and creation_mode == 1:
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
            
            
            if rayPos[0] > 50.0 and creation_mode == 2: # For the building editor
                
                # X axis
                if rayNormal[0] == 1:
                    preview_space.worldPosition = [0.0, 0.0, 0.0]
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayObj.worldPosition.z]
                if rayNormal[0] == -1:
                    preview_space.worldPosition = [0.0, 0.0, 0.0]
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayObj.worldPosition.z]
                
                # Y axis
                if rayNormal[1] == 1:
                    preview_space.worldPosition = [0.0, 0.0, 0.0]
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayObj.worldPosition.z]
                if rayNormal[1] == -1:
                    preview_space.worldPosition = [0.0, 0.0, 0.0]
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y , rayObj.worldPosition.z]
                    
                # Z axis
                if rayNormal[2] == 1:
                    preview_space.worldPosition = [0.0, 0.0, 0.0]
                    preview_block.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayObj.worldPosition.z]
                
                move_block_to_preview()
                #print(preview_block.worldPosition)
                    
            
        if R.positive and not Lshift.positive and not Rshift.positive:  # Rotate only the preview object
            own.applyRotation([0,0,math.pi/2])
            
        if R.positive and Lshift.positive or R.positive and Rshift.positive:      # Rotate the mouse over object
            rayObj.applyRotation([0,0,-math.pi/2])
        
        included_objects = ['grid_block', 'grid_building', 'wall', 'floor', 'window', 'door', 'stair', 'furniture', 'appliance']        
        if left_click.positive :                 # Place an item on the preview's spot
            #if rayPos[0] < 50.0 and rayObj["type"] == "grid_block" or rayObj["type"] == "wall" or rayObj["type"] == "floor" or rayObj["type"] == "stair" :
            #if rayPos[0] < 50.0 and rayObj["type"] == "grid_block" or rayObj["type"] == "wall" or rayObj["type"] == "floor" or rayObj["type"] == "stair" :
            if creation_mode == 1 and rayPos[0] > -50.0 and rayObj["type"] != "button":
                obj = scene.addObject(selected_part, preview_space, 0)
                obj.worldPosition = preview_space.worldPosition
                obj.worldOrientation = preview_space.worldOrientation
                obj["ID"] = random.randint(100000,999999) # give a unique ID number
            if creation_mode == 2 and rayPos[0] > 50.0 and rayObj["type"] != "button":
                #create_object_list("bathroom20180727112525.csv")
                #create_initial_block()
                place_block()
                print(rayObj["type"])
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
                    
            
        if right_click.positive: 
            if rayObj["ID"] != 0:   # Delete object (exclude grid, previews and placeholders)
                rayObj.endObject()
                previous_object = scene.objects["ground.block_editor"]
            
            if Lctrl.positive and rayObj["ID"] != 0:   # Delete object (exclude grid, previews and placeholders)
                    for object in scene.objects:
                        if object["ID"] == rayObj["ID"]:
                            object.endObject()
                    previous_object = scene.objects["ground.block_editor"]


def reset_previous_object():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    
    if mouse_over.positive and left_click.positive:
        global previous_object
        previous_object = scene.objects["ground.block_editor"]
        print(previous_object)


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

def clear_previous_buttons():
    
    placeholder_wall_button = ["placeholder.wall."+str("{0:0=3d}".format(o)) for o in range(0, 10)]
    placeholder_floor_button = ["placeholder.floor."+str("{0:0=3d}".format(o)) for o in range(0, 10)]
    
    for i in range(0, 10):
        wall_placeholder = scene.objects[placeholder_wall_button[i]]
        wall_placeholder.replaceMesh("placeholder.parts.default")
        
        floor_placeholder = scene.objects[placeholder_floor_button[i]]
        floor_placeholder.replaceMesh("placeholder.parts.default")
        
    placeholder_window_button = ["placeholder.window."+str("{0:0=3d}".format(o)) for o in range(0, 5)]
    
    for i in range(0, 5):
        window_placeholder = scene.objects[placeholder_window_button[i]]
        window_placeholder.replaceMesh("placeholder.parts.default")


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
        scene.objects["preview.parts_space"]["mode"] = 1
        ID = own["ID"]
        #print("Placeholder's ID is:",own["ID"])
        #print(own.name)
        global selected_part
        if "wall" in own.name: 
            selected_part = selected_set[0][ID]
        if "floor" in own.name: 
            selected_part = selected_set[1][ID]
        if "window" in own.name: 
            selected_part = selected_set[2][ID]
        selected_item.worldPosition = own.worldPosition
        #print(selected_set)


def preview_mesh():
    """Function to change the preview mesh to the currently selected."""

    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    global selected_part
    own.replaceMesh(selected_part)
    
    
available_sets = (set001, set002, set003, set004, set005, set006)

def change_set():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    set_number = own["set"]
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]

    global selected_set
    
    if mouse_over.positive and left_click.positive:
        print("CURRENT SET:",set_number)
        
        selected_set = available_sets[set_number]
        
        clear_previous_buttons()
        
        create_parts_buttons(available_sets[set_number][0], "wall", 9)
        create_parts_buttons(available_sets[set_number][1], "floor", 9)
        create_parts_buttons(available_sets[set_number][2], "window", 4)
        