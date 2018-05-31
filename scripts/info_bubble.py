import bge
from bge import logic

def bubble_visibility():
    
    ### CONTROLLER - The controller
    controller = bge.logic.getCurrentController()
    #print ("The controller is:",controller)
    own = controller.owner
    #print ("The owner is:",own)
    scene = bge.logic.getCurrentScene()
    #print ("The scene is:",scene)
    ### SENSORS - Mouse Over
    mouse_over_button = controller.sensors["mouse_over_button"]

    id = own["ID"]
    #print ("Object id is:",id)
    
    bubble = "bubble."+str(id)
    #print ("Bubble is:",bubble)
    
    bubble_visibility = scene.objects[bubble]["VIS"]
    print (bubble_visibility)
    #visibility = bubble["ID"]
    #print (visibility)

    if mouse_over_button.positive:
        print ("Mouse over button is positive")
        scene.objects[bubble]["VIS"] = 1
    if not mouse_over_button.positive:
        print ("Mouse over button is negative")
        scene.objects[bubble]["VIS"] = 0