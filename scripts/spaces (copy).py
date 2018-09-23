import bge
import math

first_click = 0
second_click = 0

scene = bge.logic.getCurrentScene()


def create_space():
    
    global first_click
    global second_click
    global first_click_xy
    global second_click_xy
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    #print(own["room"])
    
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    
    if own["room"] == "bathroom":
        preview_space = scene.objects["preview.block_bathroom"]
    if own["room"] == "bedroom":
        preview_space = scene.objects["preview.block_bedroom"]
    if own["room"] == "kitchen":
        preview_space = scene.objects["preview.block_kitchen"]
    if own["room"] == "livingroom":
        preview_space = scene.objects["preview.block_livingroom"]
    
    object_type = mouse_over.hitObject["type"]
    #print(object_type)
    
    if mouse_over.positive and left_click.positive and object_type == "grid_building":
        
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
                
            
        if first_click == 0 and second_click == 0:
            first_click_xy = (mouse_over.hitObject.worldPosition.x, mouse_over.hitObject.worldPosition.y)
            first_click = 1
            preview_space.worldScale = [1, 1, 1]
            preview_space.worldPosition = (first_click_xy[0], first_click_xy[1], mouse_over.hitObject.worldPosition.z)
            #print("First click location:", first_click_xy)
            

def set_space_bathroom():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        scene.objects["preview.parts_space"]["room"] = "bathroom"

        
def set_space_bedroom():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        scene.objects["preview.parts_space"]["room"] = "bedroom"
    
    
def set_space_kitchen():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        scene.objects["preview.parts_space"]["room"] = "kitchen"
        
        
def set_space_livingroom():
    controller = bge.logic.getCurrentController()
    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]
    if mouse_over.positive and left_click.positive:
        scene.objects["preview.parts_space"]["room"] = "livingroom"
        