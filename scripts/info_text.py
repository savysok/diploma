import bge
import textwrap
import os
import webbrowser
from config import info_dir
from main import debug_print

# FIX TEXT RESOLUTION
def fix_text_resolution():
    """Function to fix text resolution. Default resolution is 1.0 (72dpi).
    """
    controller = bge.logic.getCurrentController()
    own = controller.owner

    if own.resolution != 8.0:
        own.resolution = 8.0

# INFO_TEXT
# Dynamically loaded info text (from txt file)
info_files = [f for f in os.listdir(info_dir) if 'txt' in f]


def show_info_text():
    """Function that shows the text in the txt files."""
    controller = bge.logic.getCurrentController()
    own = controller.owner

    scene = bge.logic.getCurrentScene()

    message_sensor = own.sensors["update_text"]

    if message_sensor.positive:
        from main import GROUP_ID

        info_file = info_files[GROUP_ID]
        info_txt = info_dir+info_file
        info_txt_open = open(info_txt, 'r')
        dynamic_text = scene.objects["info_text"]
        info_text_wrapped = textwrap.wrap(info_txt_open.read(), 160)
        dynamic_text.text = '\n'.join([l for l in info_text_wrapped])
        info_txt_open.close()

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
