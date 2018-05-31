import os
import subprocess

print ("Initializing obj export script...\n")

### FOLDERS - The folders where the files are
models_directory = os.path.abspath(__file__+'/../../models/')+'/'
#print ("Models directory is:",models_directory)
obj_directory = os.path.abspath(__file__+'/../../export/obj')+'/'
#print ("OBJ export directory is:",obj_directory)
script_directory = os.path.abspath(__file__+'/../../scripts')+'/'
#print ("OBJ export directory is:",obj_directory)
export_obj_script = script_directory+'export_obj_scipt.py'
print ("Export obj script is:",export_obj_script,"\n")

### FILES - The files in the "models" and "export" directories
groups = [g for g in os.listdir(models_directory)]
#print ("Model groups are:",groups)
print ("FILE:\n")
for g in groups:
    name = g
    files = [f for f in os.listdir(models_directory+'/'+name) if 'blend' in f]
    #print ("Files in the folder",g,"are:",files)
    for f in files:
        #print ("File(s) inside",g,"folder (is/are):",f)
        file = models_directory+name+'/'+f
        print (file)
        
        blender_arguments = [
            'blender',
            '--background',
            file,
            '--python',
            export_obj_script
            ]
        subprocess.run(blender_arguments)
        #bpy.ops.wm.open_mainfile(filepath=file) ### This is not working

subprocess.run(blender_arguments)

print ("Done.")
print ("\n\n")