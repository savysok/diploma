import bge
import math


scene = bge.logic.getCurrentScene()
      
        
def camera_move():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    up = controller.sensors["W"]
    left = controller.sensors["A"]
    down = controller.sensors["S"]
    right = controller.sensors["D"]
    
    if up.positive:
        own.worldPosition.z += 1
    if left.positive:
        own.worldPosition.x -= 0.5
        own.worldPosition.y -= 0.5
    if down.positive:
        own.worldPosition.z -= 1
    if right.positive:
        own.worldPosition.x += 0.5
        own.worldPosition.y += 0.5
    
    
def camera_zoom():
    
    controller = bge.logic.getCurrentController()
    
    mouse_wheel_up = controller.sensors["mouse_wheel_up"]
    mouse_wheel_down = controller.sensors["mouse_wheel_down"]
    
    #active_camera = scene.objects["camera.parts.isometric"]
    active_camera = controller.owner
    
    if mouse_wheel_up.positive:
        if active_camera.ortho_scale >= 12:
            active_camera.ortho_scale -= 6
            
    if mouse_wheel_down.positive:
        if active_camera.ortho_scale < 30:
            active_camera.ortho_scale += 6
            
        
z = 0

def camera_rotation():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    rot_left = controller.sensors["arrow_left"]
    rot_right = controller.sensors["arrow_right"]
    
    if rot_left.positive:
        own.applyRotation([0,0,z+math.pi/2])
    if rot_right.positive:
        own.applyRotation([0,0,z-math.pi/2])
        

cam1 = scene.objects['camera.parts.top'] # camera.parts.top
cam2 = scene.objects['camera.parts.isometric'] # camera.parts.isometric
cam3 = scene.objects['camera.building.isometric'] # camera.building.isometric
cam4 = scene.objects['camera.warehouse'] # camera.warehouse


def viewport_layout_1():
    
    width = bge.render.getWindowWidth() # screen's resolution (width)
    height = bge.render.getWindowHeight() # screen's reslution (height)
    
    #cam1.setViewport(0, 0, width, height) 
    cam2.setViewport(int(width/4), int(height/24), width, height) 
    #cam3.setViewport(1920, 0, width, height) 
    cam4.setViewport(0, int(height/24), width, height) 

    cam1.useViewport = False
    cam2.useViewport = True
    cam3.useViewport = False
    cam4.useViewport = True
    
    buttons_empty.worldPosition.y = -1

def viewport_layout_2():
    
    width = bge.render.getWindowWidth() # screen's resolution (width)
    height = bge.render.getWindowHeight() # screen's reslution (height)
    
    cam1.setViewport(int(width/4), int(height/24), int(width/2), height) # camera.parts.top
    cam2.setViewport(int(width/2), int(height/24), width, height) # camera.parts.isometric
    #cam3.setViewport(1920, 0, width, height) # camera.building.isometric
    cam4.setViewport(0, int(height/24), width, height) # camera.warehouse

    cam1.useViewport = True
    cam2.useViewport = True
    cam3.useViewport = False
    cam4.useViewport = True
    
    buttons_empty.worldPosition.y = -1
        
def viewport_layout_3():
    
    width = bge.render.getWindowWidth() # screen's resolution (width)
    height = bge.render.getWindowHeight() # screen's reslution (height)
    
    cam1.setViewport(int(width/4), int(height/2), int(width/2), height) # camera.parts.top
    cam2.setViewport(int(width/4), int(height/24), int(width/2), int(height/2)) # camera.parts.isometric
    cam3.setViewport(int(width/2), int(height/24), width, height) # camera.building.isometric
    cam4.setViewport(0, int(height/24), width, height) # camera.warehouse
    
    cam1.useViewport = True
    cam2.useViewport = True
    cam3.useViewport = True
    cam4.useViewport = True
    
    buttons_empty.worldPosition.y = 0


def block_editor_layout_1():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    left_click = controller.sensors["left_click"]
    mouse_over = controller.sensors["mouse_over"]

    if mouse_over.positive and left_click.positive:
        viewport_layout_1()
        
def block_editor_layout_2():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    left_click = controller.sensors["left_click"]
    mouse_over = controller.sensors["mouse_over"]

    if mouse_over.positive and left_click.positive:
        viewport_layout_2()
        
def building_editor_layout_1():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner

    left_click = controller.sensors["left_click"]
    mouse_over = controller.sensors["mouse_over"]

    if mouse_over.positive and left_click.positive:
        viewport_layout_3()
    

def intro_camera():
    controller = bge.logic.getCurrentController()
    #any_key = controller.sensors["AllKeys"]
    left_click = controller.sensors["left_click"]
    status = controller.owner["status"]
    print(status)
    if status == 0:
        if left_click.positive:
            scene.active_camera = scene.objects["camera.parts.isometric"]
            viewport_layout_1()
            status = 1


for buttons_scene in bge.logic.getSceneList():
    if buttons_scene.name == "GUI-BUTTONS":
        buttons_empty = buttons_scene.objects["empty.spaces_buttons.parent"]
        
        
def hide_columns():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner

    left_click = controller.sensors["left_click"]
    mouse_over = controller.sensors["mouse_over"]
    
    excluded_objects = ('placeholder', 'grid', 'button')
    
    if mouse_over.positive and left_click.positive:
        for object in scene.objects:
            if not any(excluded_objects in object.name for excluded_objects in excluded_objects):
                # bottom and top row buttons
                if object.worldPosition.x > own.worldPosition.x:
                    object["visibility"] = 0
                if object.worldPosition.x <= own.worldPosition.x:
                    object["visibility"] = 1
                    
def hide_rows():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner

    left_click = controller.sensors["left_click"]
    mouse_over = controller.sensors["mouse_over"]
    
    excluded_objects = ('placeholder', 'grid', 'button')
    
    if mouse_over.positive and left_click.positive:
        for object in scene.objects:
            if not any(excluded_objects in object.name for excluded_objects in excluded_objects):
                # bottom and top row buttons
                if object.worldPosition.y < own.worldPosition.y:
                    object["visibility"] = 0
                if object.worldPosition.y >= own.worldPosition.y:
                    object["visibility"] = 1
                
def unhide_all_objects():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner

    left_click = controller.sensors["left_click"]
    mouse_over = controller.sensors["mouse_over"]

    if mouse_over.positive and left_click.positive:
        for object in scene.objects:
            object["visibility"] = 1
            
            
def fullscreen():
    
    print("Working on it")
    
    
#print(bge.app.version)
#print(bge.app.version_string)
#print(bge.app.version_char)
#print(bge.render.getDisplayDimensions())
#bge.render.setFullScreen(True)
#bge.render.setWindowSize(800, 600)
#bge.render.showProperties(True)