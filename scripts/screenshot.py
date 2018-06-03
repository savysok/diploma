import bge
import subprocess
import time
from config import screenshot_dir


def take_screenshot():
    """Function to take a screenshot.
    Requires Imagemagick in Linux.
    Windows support is in the TODO list.
    """
    controller = bge.logic.getCurrentController()
    own = controller.owner

    scene = bge.logic.getCurrentScene()

    mouse_over_button = own.sensors["mouse_over_button"]
    left_click_button = own.sensors["left_click_button"]

    date = time.strftime("%Y%m%d_%H%M%S_")
    screenshot = screenshot_dir+date+'scrnsht.jpg'

    screenshot_args = [
        'import',
        '-window',
        'root',
        '-resize',
        '1920x1280',
        '-delay',
        '200',
        screenshot
        ]

    if mouse_over_button.positive and left_click_button.positive:
        subprocess.run(screenshot_args)
