import bge
import math
import mathutils

def camera_control(camera_placeholder):
    
    controller = bge.logic.getCurrentController()
    #print ("The controller is:",controller)
    own = controller.owner
    #print ("The owner is:",own)
    scenes = bge.logic.getSceneList()

    ### SENSORS - Left Click and Mouse Over
    left_click_button = controller.sensors["left_click_button"]
    mouse_over_button = controller.sensors["mouse_over_button"]
        
    ### STATUS = 0: closed, 1: opened
    status = own["STATUS"]
    #print ("Status is:",status)
    
    rotate_left = mathutils.Euler((0, 0, math.radians(90)), "XYZ")
    #print ("Left rotation is:",rotate_left)
    rotate_right = mathutils.Euler((0, 0, -math.radians(90)), "XYZ")
    #print ("Right rotation is:",rotate_right)
    
    if mouse_over_button.positive and left_click_button.positive:
        
        print ("The mouse is over the button and clicked.\n")
        #print ("Scenes are:",scenes)
        
        for scene in scenes:
            if scene.name == "MAIN":
                #print ("Scene is:",scene.name)
                camera = scene.objects["camera.MAIN"]
                #print ("Camera is",camera)
                placeholder = scene.objects[camera_placeholder]
                print ("Placeholder is:",placeholder)
                rotation = placeholder.worldOrientation.to_euler()
                print ("Rotation is:",rotation.z)
                if status == 0:
                    placeholder.worldOrientation = camera.worldOrientation
                    #print ("Placeholder's world orientation is:",placeholder.worldOrientation)
                    ### Put function here. TODO
                    own["STATUS"] = 1
                    print (scene.name,"'s status is",status,". Buttons are visible\n")
                if status == 1:
                    ### Put function here. TODO
                    placeholder.localOrientation = rotate_left.to_matrix()
                    own["STATUS"] = 0
                    print (scene.name,"'s status is",status,". Buttons are hidden\n")

def camera_control_buldings():
    camera_control("parent.buttons.buildings.001")   

def camera_control_parts():
    camera_control("parent.buttons.parts.001")      
    
def camera_control_grids():
    camera_control("parent.buttons.grids.001")