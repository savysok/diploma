import subprocess
import time
import os

def take_screenshot():
    screenshot_directory = os.path.abspath(__file__+'/../../screenshots')+'/'

    #date = datetime.date.today()
    date = time.strftime("%Y%m%d_%H%M%S_")
    screenshot = screenshot_directory+date+'scrnsht.jpg'

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
        
    subprocess.run(screenshot_args)