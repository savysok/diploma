import bge
import camera
from camera import block_editor_layout_1, building_editor_layout_1

scenes = bge.logic.getSceneList()

for scene in scenes:
    if scene.name == "MAIN":
        main_scene = scene
    if scene.name == "GUI-BUTTONS":
        gui_scene = scene

def extra_buttons(show_x, hide_x, empty):

    controller = bge.logic.getCurrentController()
    own = controller.owner

    mouse_over = controller.sensors["mouse_over"]
    left_click = controller.sensors["left_click"]

    if mouse_over.positive and left_click.positive:

        status = own["status"]

        if status == "closed":
            empty.worldPosition.x = 1.575
            own["status"] = "open"
        if status == "open":
            empty.worldPosition.x = 3.0
            own["status"] = "closed"
            
        main_scene.objects["preview.parts_default"]["mode"] = 2

#def save_button_menu():
#    empty = scene.objects["empty.buttons.save"]
#    extra_buttons(1.3, 3.0, scene.objects["empty.buttons.save"])


