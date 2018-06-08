import bge
import math
import mathutils
from main import debug_print


# BUTTON_BEHAVIOUR
def placeholder_position(buttons_parent):
    """Function that controls the movement of the empties that
    are parents to the parts, grids and buildings objects.
    """
    controller = bge.logic.getCurrentController()
    own = controller.owner

    scenes = bge.logic.getSceneList()

    left_click_button = controller.sensors["left_click_button"]
    mouse_over_button = controller.sensors["mouse_over_button"]

    status = own["STATUS"]  # STATUS:  0 = closed, 1 = opened
    debug_print ("Status is:",status)

    rotate_left = mathutils.Euler((0, 0, math.radians(90)), "XYZ")
    rotate_right = mathutils.Euler((0, 0, -math.radians(90)), "XYZ")

    if mouse_over_button.positive and left_click_button.positive:

        for scene in scenes:
            if scene.name == "MAIN":
                camera = scene.objects["camera.MAIN"]
                placeholder = scene.objects[buttons_parent]
                rotation = placeholder.worldOrientation.to_euler()
                
                if status == 0:
                    placeholder.worldOrientation = camera.worldOrientation
                    own["STATUS"] = 1
                    debug_print (scene.name,"'s status is",status,". Buttons are visible\n")
                    
                if status == 1:
                    placeholder.localOrientation = rotate_left.to_matrix()
                    own["STATUS"] = 0
                    debug_print (scene.name,"'s status is",status,". Buttons are hidden\n")


def placeholder_buldings():
    placeholder_position("parent.buttons.buildings.001")


def placeholder_parts():
    placeholder_position("parent.buttons.parts.001")


def placeholder_grids():
    placeholder_position("parent.buttons.grids.001")
    

def extra_buttons(placeholder_item):
    """Function that controls the movement of the empties that
    are parents to the Save, Load and Export buttons.
    """
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    scene = bge.logic.getCurrentScene()
    
    mouse_over_button = controller.sensors["mouse_over_button"]

    status = own["STATUS"]  # STATUS:  0 = closed, 1 = opened
    
    placeholder = scene.objects[placeholder_item]
    
    save_button = scene.objects["button.save.001"]
    
    if mouse_over_button.positive and status == 0:
        print("It's working. 0")
        placeholder.worldPosition.x = 6.3
        own["STATUS"] = 1
        
    if mouse_over_button.positive and status == 1:
            print("It's working. 1")
            placeholder.worldPosition.x = 10
            own["STATUS"] = 0
            
def save_buttons():
    extra_buttons("parent.buttons.save")
    
    
    
    
    
        
    