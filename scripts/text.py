import bge

def text_box(new_text):
    scene_list = bge.logic.getSceneList()
    for scene in scene_list:
        if scene.name == "GUI-BUTTONS":
            text_scene = scene
            info_text_box = text_scene.objects["info_text"].text = new_text

def text_resolution():
    scene = bge.logic.getCurrentScene()
    info_text = scene.objects["info_text"]
    scene.objects["info_text"].resolution = 4
    info_text.resolution = 8
    
def block_editor_text_1():
    text_box("BLOCK EDITOR - Layout 1 (Isometric View)")
    
def block_editor_text_2():
    text_box("BLOCK EDITOR - Layout 2 (Split screen: Isometric and Top views")
    
def building_editor_text_1():
    text_box("BUILDING EDITOR - Layout 1")