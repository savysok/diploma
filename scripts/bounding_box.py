import bge


def bounding_box_visibility():
    """Function to hide or show the bounding box object."""
    controller = bge.logic.getCurrentController()
    own = controller.owner

    H = controller.sensors["H"]

    visibility = own["visibility"]

    for scene in bge.logic.getSceneList():
        if scene.name == "MAIN":
            if H.positive and visibility == 0:
                for obj in scene.objects:
                    if obj.name == "bounding_box":
                        obj.visible = False
                own["visibility"] = 1

            if H.positive and visibility == 1:
                for obj in scene.objects:
                    if obj.name == "bounding_box":
                        obj.visible = True
                own["visibility"] = 0
