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
    text_box("BLOCK EDITOR - Αξονομετρική προβολή")
    
def block_editor_text_2():
    text_box("BLOCK EDITOR - Αξονομετρική προβολή + Κάτοψη")
    
def building_editor_text_1():
    text_box("BUILDING EDITOR - Χωροθέτης")
    
def button_exit():
    text_box("Έξοδος από το πρόγραμμα")
    
def button_reload():
    text_box("Επανεκκίνηση του προγράμματος")
    
def button_save_load():
    text_box("Αποθήκευση και Φόρτωση του μοντέλου")
    
def button_screenshot():
    text_box("Αποθήκευση εικόνας στον φάκελο screenshots")    
    
def button_viewport():
    text_box("Διαχωρισμός του περιβάλλοντος εργασίας (μη-ενεργό)")
    
def button_block():
    text_box("Φόρτωση έτοιμου block")    

def button_hide_show():
    text_box("Απόκρυψη/Εμφάνιση σειρών/στηλών")
    
def button_fullscreen():
    text_box("Λειτουργία πλήρους οθόνη")