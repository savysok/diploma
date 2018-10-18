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
    text_box("Αποθήκευση (αριστερό κλικ) και Φόρτωση (δεξί κλικ) του μοντέλου")
    
def button_screenshot():
    text_box("Αποθήκευση εικόνας στον φάκελο screenshots")    
    
def button_viewport():
    text_box("Διαχωρισμός του περιβάλλοντος εργασίας (μη-ενεργό)")
    
def button_block():
    text_box("Φόρτωση έτοιμου block")    

def button_hide_show():
    text_box("Απόκρυψη/Εμφάνιση σειρών/στηλών και επιπέδων καθ'ύψος")
    
def button_fullscreen():
    text_box("Λειτουργία πλήρους οθόνη")
    
def button_clear_all():
    text_box("Καθαρισμός όλων")
    
def button_clear_spaces():
    text_box("Καθαρισμός των χώρων")
    
def button_show_level_zero():
    text_box("Εμφάνιση πρώτου επιπέδου (Level 0)")
    
def button_show_level_one():
    text_box("Εμφάνιση δεύτερου επιπέδου (Level 1)")
    
def button_show_level_two():
    text_box("Εμφάνιση τρίτου επιπέδου (Level 2)")
    
def button_show_level_three():
    text_box("Εμφάνιση τέταρτου επιπέδου (Level 3)")
    
def button_sets_set1():
    text_box("Δάπεδα 1 | Εξωτερικοί Τοίχοι | Κουφώματα")
    
def button_sets_set2():
    text_box("Δάπεδα 2 | Εσωτερικοί Τοίχοι (πρώτη και δεύτερη σειρά, περασιά στο κέντρο, τρίτη σειρά στο άκρο")
    
def button_sets_set3():
    text_box("Δάπεδα 3 | Σκάλες | Κολώνες")
    
def button_sets_set4():
    text_box("(κενό)")
    
def button_sets_set5():
    text_box("Έπιπλα Κουζίνας")
    
def button_sets_set6():
    text_box("Έπιπλα Κρεβατοκάμαρας")