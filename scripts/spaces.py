import bge
import math
from grid import clear_block_grid, create_grid_pattern

first_click = 0
second_click = 0
distance_x = 0
distance_y = 0

bathroom_dimensions = (0, 0)
bedroom_dimensions = (0, 0)
kitchen_dimensions = (0, 0)
livingroom_dimensions = (0, 0)

#scene = bge.logic.getCurrentScene()
for scene_list in bge.logic.getSceneList():
    if scene_list.name == "MAIN":
        scene = scene_list

def create_space():
    
    global first_click
    global second_click
    global first_click_xy
    global second_click_xy
    global distance_x
    global distance_y
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    #print(own["room"])
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    right_click = controller.sensors["right_click"]
    
    if own["room"] == "bathroom":
        preview_space = scene.objects["preview.block_bathroom"]
    if own["room"] == "bedroom":
        preview_space = scene.objects["preview.block_bedroom"]
    if own["room"] == "kitchen":
        preview_space = scene.objects["preview.block_kitchen"]
    if own["room"] == "livingroom":
        preview_space = scene.objects["preview.block_livingroom"]
    
    if mouse_over.positive and left_click.positive and mouse_over.hitObject["type"] == "grid_building":
        
        if first_click == 1 and second_click == 1:
            #print("Resetting the click counters")
            first_click = 0
            second_click = 0
        
        if first_click == 1 and second_click == 0:
            second_click_xy = (mouse_over.hitObject.worldPosition.x, mouse_over.hitObject.worldPosition.y)
            second_click = 1
            #print("Second click location:",second_click_xy)
            
            if first_click_xy[0] <= second_click_xy[0]:
                if first_click_xy[1] >= second_click_xy[1]:
                    distance_x = first_click_xy[0] - second_click_xy[0] - 1
                    distance_y = first_click_xy[1] - second_click_xy[1] + 1
                    #print("Distances are:", distance_x, distance_y)
                    preview_space.worldPosition = (first_click_xy[0]-distance_x/2-0.5, first_click_xy[1]-distance_y/2+0.5, mouse_over.hitObject.worldPosition.z)
                    preview_space.worldScale = [abs(distance_x), abs(distance_y), 1]
                    #print(preview_space.worldScale)
                if first_click_xy[1] < second_click_xy[1]:
                    distance_x = first_click_xy[0] - second_click_xy[0] - 1
                    distance_y = first_click_xy[1] - second_click_xy[1] - 1
                    #print("Distances are:", distance_x, distance_y)
                    preview_space.worldPosition = (first_click_xy[0]-distance_x/2-0.5, first_click_xy[1]-distance_y/2-0.5, mouse_over.hitObject.worldPosition.z)
                    preview_space.worldScale = [abs(distance_x), abs(distance_y), 1]
                    #print(preview_space.worldScale)    
            
            if first_click_xy[0] > second_click_xy[0]:
                if first_click_xy[1] >= second_click_xy[1]:
                    distance_x = first_click_xy[0] - second_click_xy[0] + 1
                    distance_y = first_click_xy[1] - second_click_xy[1] + 1
                    #print("Distances are:", distance_x, distance_y)
                    preview_space.worldPosition = (first_click_xy[0]-distance_x/2+0.5, first_click_xy[1]-distance_y/2+0.5, mouse_over.hitObject.worldPosition.z)
                    preview_space.worldScale = [abs(distance_x), abs(distance_y), 1]
                    #print(preview_space.worldScale)
                if first_click_xy[1] < second_click_xy[1]:
                    distance_x = first_click_xy[0] - second_click_xy[0] + 1
                    distance_y = first_click_xy[1] - second_click_xy[1] - 1
                    #print("Distances are:", distance_x, distance_y)
                    preview_space.worldPosition = (first_click_xy[0]-distance_x/2+0.5, first_click_xy[1]-distance_y/2-0.5, mouse_over.hitObject.worldPosition.z)
                    preview_space.worldScale = [abs(distance_x), abs(distance_y), 1]
                    #print(preview_space.worldScale) 
            #print(distance_x, distance_y)
            
            if own["room"] == "bathroom":
                global bathroom_dimensions
                bathroom_dimensions = (distance_x, distance_y)
                print("Bathroom dimensions:",bathroom_dimensions)
            if own["room"] == "bedroom":
                global bedroom_dimensions
                bedroom_dimensions = (distance_x, distance_y)
                print("Bedroom dimensions",bedroom_dimensions)
            if own["room"] == "kitchen":
                global kitchen_dimensions
                kitchen_dimensions = (distance_x, distance_y)
                print("Kitchen dimensions",kitchen_dimensions)
            if own["room"] == "livingroom":
                global livingroom_dimensions
                livingroom_dimensions = (distance_x, distance_y)
                print("Livingroom dimensions",livingroom_dimensions)
                
            
        if first_click == 0 and second_click == 0:
            first_click_xy = (mouse_over.hitObject.worldPosition.x, mouse_over.hitObject.worldPosition.y)
            first_click = 1
            preview_space.worldScale = [1, 1, 1]
            preview_space.worldPosition = (first_click_xy[0], first_click_xy[1], mouse_over.hitObject.worldPosition.z)
            #print("First click location:", first_click_xy)
            
            
def create_space_bathroom():
    print("TODO")
    
def create_space_bedroom():
    print("TODO")
    
def create_space_kitchen():
    print("TODO")
    
def create_space_livingroom():
    print("TODO")


# Set the room space

def set_space(room):
    """Function that sets the active room for the create_space() function"""
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        scene.objects["preview.parts_space"]["room"] = room

def set_space_bathroom():
    set_space("bathroom")
        
def set_space_bedroom():
    set_space("bedroom")
    
def set_space_kitchen():
    set_space("kitchen")

def set_space_livingroom():
    set_space("livingroom")


# Reset the position and scale of the room preview block
def reset_space(preview_space, position_x):
    """Function that resets the room preview space back to it's original position"""
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        scene.objects[preview_space].worldPosition = [position_x, 0, -50]
        scene.objects[preview_space].worldScale = [1, 1, 1] 
        #distance_x = 0
        #distance_y = 0

def reset_space_bathroom():
    reset_space("preview.block_bathroom", 100)

def reset_space_bedroom():
    reset_space("preview.block_bedroom", 102)

def reset_space_kitchen():
    reset_space("preview.block_kitchen", 104)

def reset_space_livingroom():
    reset_space("preview.block_livingroom", 106)
    

def reset_spaces():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        reset_space("preview.block_bathroom", 100)
        reset_space("preview.block_bedroom", 102)
        reset_space("preview.block_kitchen", 104)
        reset_space("preview.block_livingroom", 106)
        clear_previous_room()
        clear_block_grid()
        create_grid_pattern(6, 6, 0, "grid_block")

def reset_block_grid():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        clear_previous_room()
        clear_block_grid()
        create_grid_pattern(6, 6, 0, "grid_block")
        
# Create the room grid at the block editor
def room_grid(room, dimension_x, dimension_y):
    """Function that creates the grid patternt at the block editor"""
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        if distance_x != 0: 
            clear_block_grid()
            create_grid_pattern(abs(dimension_x)/2, abs(dimension_y)/2, 0, room)
      
      
def clear_previous_room():
    
    object_types = ('wall', 'floor', 'window', 'door', 'furniture', 'appliance')
    
    for object in scene.objects:
        if any(object_types in object.name for object_types in object_types) and object.worldPosition.x < 50 and object.worldPosition.x >= -50:
            object.endObject()
    
      
def bathroom_grid():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        clear_previous_room()
        room_grid("grid_block.bathroom", bathroom_dimensions[0], bathroom_dimensions[1])
            
def bedroom_grid():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        clear_previous_room()
        room_grid("grid_block.bedroom", bedroom_dimensions[0], bedroom_dimensions[1])
            
def kitchen_grid():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        clear_previous_room()
        room_grid("grid_block.kitchen", kitchen_dimensions[0], kitchen_dimensions[1])
            
def livingroom_grid():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        clear_previous_room()
        room_grid("grid_block.livingroom", livingroom_dimensions[0], livingroom_dimensions[1])
        
        
def recreate_room():
    print("Recreating the rooms")