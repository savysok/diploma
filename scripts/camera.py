import bge
import math

scene = bge.logic.getCurrentScene()

            
def select_camera():
    
    controller = bge.logic.getCurrentController()
    
    facade = controller.sensors["F"] # front view (orthographic)
    top = controller.sensors["T"] # top view (orthographic)
    corner = controller.sensors["C"] # corner view (isometric)
    
    if facade.positive:
        print("Switching to the facade camera")
        scene.active_camera = scene.objects["camera.parts.facade"]
        
    if top.positive:
        print("Switching to the top camera")
        scene.active_camera = scene.objects["camera.parts.top"]
        
    if corner.positive:
        print("Switching to the isometric")
        scene.active_camera = scene.objects["camera.parts.isometric"]
      
        
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
        if active_camera.ortho_scale >= 24:
            active_camera.ortho_scale -= 6
            
    if mouse_wheel_down.positive:
        if active_camera.ortho_scale < 24:
            active_camera.ortho_scale += 6
            

def active_editor():
    
    controller = bge.logic.getCurrentController()
    
    block_editor = controller.sensors["Key1"]
    building_editor = controller.sensors["Key2"]
    
    cam1 = scene.objects['camera.parts.top']
    cam2 = scene.objects['camera.parts.isometric']
    cam3 = scene.objects['camera.building.isometric']
    cam4 = scene.objects['camera.warehouse']
    
    width = bge.render.getWindowWidth()
    height = bge.render.getWindowHeight()
    
    if block_editor.positive:
        #scene.active_camera = scene.objects["camera.parts.isometric"]
        #split_screen()
                #split_screen_2()
        cam1.setViewport(0, 0, int(width/2), height) # camera.parts.top
        cam2.setViewport(int(width/2), 0, width, height) # camera.parts.isometric
        cam3.setViewport(1920, 0, width, height) # camera.building.isometric
        cam4.setViewport(0, 0, width, height) # camera.warehouse

        cam1.useViewport = True
        cam2.useViewport = True
        cam3.useViewport = False
        cam4.useViewport = True
        
    if building_editor.positive:
        #scene.active_camera = scene.objects["camera.building.isometric"]
        #split_screen_2()
        cam1.setViewport(120, 0, int(width/3), int(height/2)) # camera.parts.top
        cam2.setViewport(120, int(height/2), int(width/3), height) # camera.parts.isometric
        cam3.setViewport(int(width/3), 0, width, height+120) # camera.building.isometric
        cam4.setViewport(0, 0, width, height) # camera.warehouse
        
        cam1.useViewport = True
        cam2.useViewport = True
        cam3.useViewport = True
        cam4.useViewport = True
        
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
        

def intro_camera():
    controller = bge.logic.getCurrentController()
    #any_key = controller.sensors["AllKeys"]
    left_click = controller.sensors["left_click"]
    status = controller.owner["status"]
    print(status)
    if status == 0:
        if left_click.positive:
            scene.active_camera = scene.objects["camera.parts.isometric"]
            status = 1
