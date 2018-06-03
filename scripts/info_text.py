import bge
import webbrowser
from config import info_dir
from main import debug_print, info_files

# FIX TEXT RESOLUTION
def fix_text_resolution():
    """Function to fix text resolution. Default resolution is 1.0 (72dpi).
    """
    controller = bge.logic.getCurrentController()
    own = controller.owner

    if own.resolution != 32.0:
        own.resolution = 32.0

# WIKIPEDIA
def open_wikipedia_link():
    """Function to open wikipedia link in the web browser."""
    controller = bge.logic.getCurrentController()
    own = controller.owner

    scene = bge.logic.getCurrentScene()

    mouse_over_button = own.sensors["mouse_over_button"]
    left_click_button = own.sensors["left_click_button"]

    if mouse_over_button.positive and left_click_button.positive:
        
        from main import GROUP_ID

        info_file = info_files[GROUP_ID]
        info_txt = info_dir+info_file
        
        info_txt_open = open(info_txt, 'r')
        
        url = info_txt_open.readline()
        webbrowser.open(url)
