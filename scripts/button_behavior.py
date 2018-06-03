import bge
import math
import mathutils


# DEBUGGING
DEBUG=False
print("(Debugging is set to", DEBUG, ")\n")
def debug_print(*args):
    """Function that set the debugging mode On (True) or Off (False)"""
    if DEBUG:
        print(*args)


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

    status = own["STATUS"]  # STATUS = 0: closed, 1: opened
    debug_print ("Status is:",status)

    rotate_left = mathutils.Euler((0, 0, math.radians(90)), "XYZ")
    debug_print ("Left rotation is:",rotate_left)
    rotate_right = mathutils.Euler((0, 0, -math.radians(90)), "XYZ")
    debug_print ("Right rotation is:",rotate_right)

    if mouse_over_button.positive and left_click_button.positive:

        debug_print ("The mouse is over the button and clicked.\n")

        for scene in scenes:
            if scene.name == "MAIN":
                camera = scene.objects["camera.MAIN"]
                placeholder = scene.objects[buttons_parent]
                debug_print ("Placeholder is:",placeholder)
                rotation = placeholder.worldOrientation.to_euler()
                debug_print ("Rotation is:",rotation.z)
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
