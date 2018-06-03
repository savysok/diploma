import bge

def rotate_cube():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    own.applyRotation([0.003, 0.005, 0.001])