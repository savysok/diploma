def list_all_objects():
    """Copied from 
    https://blender.stackexchange.com/questions/31413/how-to-list-all-scenes-objects-sensors-controllers-actuators-etc
    """
    scenes = bge.logic.getSceneList()
    for scene in scenes :
        print("scene : %s"%scene.name)
        for obj in scene.objects :
            print("   object : %s"%obj.name)
            for sensor in obj.sensors :
                print("      sensor : %s"%sensor.name)  
            for cont in obj.controllers :
                print("      controller : %s"%cont.name)      
            for actu in obj.actuators :
                print("      actuator : %s"%actu.name) 
                
                
                
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
        
        
        
        
    #scene = bge.logic.getCurrentScene()
    
    #mesh_objects = ['lamp', 'sun', 'camera', 'preview', 'placeholder', 'ground', 'grid', 'background', 'empty', 'origin', 'selected', 'button']
    
    #for obj in scene.objects:
    #    if not any(mesh_objects in obj.name for mesh_objects in mesh_objects):
            #print(obj.name)
            #print(obj.meshes[0].getPolygon(1))
            #print(obj.meshes[0].getVertex(0, 1))
            #print(obj.meshes[0].numPolygons)
    #        print("Working on it..")
            #print(obj.meshes[0].getPolygon(0).getMaterial())
            #print(obj.meshes[0].getVertex(0, 0).getXYZ())
            #print(obj.meshes[0].getVertex(0, 0).normal)
            
            
        
        
        
        
        #obj.setVisible(0)

    

    
    #scene.world.ambientColor = [ 0.5, 0.5, 0.0 ]