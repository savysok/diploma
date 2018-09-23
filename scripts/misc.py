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
                