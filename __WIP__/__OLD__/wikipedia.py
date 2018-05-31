### Code to check the python version used.
#import sys
#print(sys.version,"\n")

import bge
import os
import webbrowser

info_directory = os.path.abspath(__file__+'/../../info')

new_ID = 1

info_files = [f for f in os.listdir(info_directory) if 'info' in f]
#print ("Info files inside the info folder are:",info_files)
info_file = info_files[new_ID]
print ("Selected file is:",info_file,"\n")
info_txt = info_directory+"/"+info_file
#print ("Info file path is:",info_txt)
print ("Opening info file for reading..")
info_txt_open = open(info_txt, 'r')
print ("Done.")

wiki_files = [f for f in os.listdir(info_directory) if 'wiki' in f]
#print ("Info files inside the info folder are:",info_files)
wiki_file = wiki_files[new_ID]
print ("Selected file is:",wiki_file,"\n")
wiki_txt = info_directory+"/"+wiki_file
#print ("Wiki file path is:",wiki_txt)
print ("Opening wiki file for reading..")
wiki_txt_open = open(wiki_txt, 'r')
print ("Done.")

def show_text():
    
    controller = bge.logic.getCurrentController()
    #print ("The controller is:",controller)
    own = controller.owner
    #print ("The owner is:",own)
    
    scene = bge.logic.getCurrentScene()
    #print ("Current scene is:",scene)
    
    dynamic_text = scene.objects["info_text"]
    
    dynamic_text.text = info_txt_open.read()
    info_txt_open.close()

def go_to_wikipedia():

    controller = bge.logic.getCurrentController()
    #print ("The controller is:",controller)
    own = controller.owner
    #print ("The owner is:",own)
    
    scene = bge.logic.getCurrentScene()
    #print ("Current scene is:",scene)
    
    left_click_button = controller.sensors["left_click_button"]
    mouse_over_button = controller.sensors["mouse_over_button"]
    
    if left_click_button.positive and mouse_over_button.positive:
        print ("Wikipedia link has been clicked. Opening webpage")
        webbrowser.open(wiki_txt_open.read())