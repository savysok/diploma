import bge
from random import randint

x = randint(-10,10)/1000
y = randint(-10,10)/1000
z = randint(-10,10)/1000

def rotate_cube():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner

    own.applyRotation([x,y,z])
    