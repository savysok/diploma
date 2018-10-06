import bge
import os
import subprocess
import sys
from config import *
from save_block import save_function
import time

export_stl_script = scripts_dir+'export_stl.py'

def export_stl():
    
    controller = bge.logic.getCurrentController()
    
    E = controller.sensors["E"]
    
    exporter = os.path.abspath(scripts_dir+'../3dprint.blend')
    
    date = time.strftime("%Y%m%d%H%M%S")
    save_function("block"+date+".csv")
    
    if E.positive:
        blender_arguments = [
            'blender',
            '--background',
            exporter,
            '--python',
            export_stl_script
            ]
            
        subprocess.run(blender_arguments)
    
export_stl()