import bge

def rotate_cube():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    scene = bge.logic.getCurrentScene()
    #rotating_cube = scene.objects["rotating_cube.001"]
    
    own.applyRotation([0.003, 0.005, 0.001])