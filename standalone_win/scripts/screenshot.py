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

    mouse_over = own.sensors["mouse_over"]
    left_click = own.sensors["left_click"]

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

    if mouse_over.positive and left_click.positive:
        subprocess.run(screenshot_args)
