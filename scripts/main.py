### IMPORT - Importing the necessary modules ###
###### START ######
import bge                      ### bge - The Blender Game Engine
import csv                      ### csv - The CSV Library for parsing the csv file
import os                       ### os - To find the path names (WIP)
import subprocess               ### subprocess - Executes system functions. Used mainly for the screenshots with Imagemagick.
import textwrap                 ### textwrap - Text wrapper (for the info section)
import time                     ### time - Needed for the date/time format at the screenshots.
import webbrowser               ### webbrowser - Opens a web browser (will be used to open wikipedia pages)
from bge import logic           ### logic - Needed to load external files
from csv import DictReader      ### DictReader - DictReader is needed to read the csv file's columns
### Custom scripts ###          ### Custom scripts go here

###### END ######

### PHASE 1: INITIALIZATION ###

print("\n\n\n::INITIALIZATION::")
print("Initializing the main script...\n")
print(":::PHASE 1:::\n")

### PATHS - Get the absolute directories of the folders
print("::DIRECTORIES::")
print("Getting the directories...")
data_directory = os.path.abspath(__file__+'/../../data')+'/'
#print("DATA:\n",data_directory)
models_directory = os.path.abspath(__file__+'/../../models')+'/'
#print("MODELS:\n",models_directory)
info_directory = os.path.abspath(__file__+'/../../info')+'/'
#print("MODELS:\n",info_directory)
custom_directory = os.path.abspath(__file__+'/../../custom')+'/'
#print("CUSTOM:\n",custom_directory)
textures_directory = os.path.abspath(__file__+'/../../textures')+'/' ### Not needed for now
#print("TEXTURES:\n",textures_directory)
screenshot_directory = os.path.abspath(__file__+'/../../screenshots')+'/'
#print("TEXTURES:\n",textures_directory)
print("Done.\n")

### GROUP - The group at which the object(s) belong. The grouping is sorted by the folders in the "models" subfolder.
print("::GROUPS::")
groups = [g for g in os.listdir(models_directory)]      ### Get a list of all the subfolders in the "models" folder
max_GROUP_ID = len(groups)                              ### Get the maximum number of subfolders
print("There are",max_GROUP_ID,"groups of models.")
GROUP_ID=0                                              ### An "id" variable to select the different groups
print("The groups are:")
for g in groups:
    print(" ",g)
print("The active group is:",groups[GROUP_ID])
print("Done.\n")


### Function to change the group of items
def change_group():

    controller = bge.logic.getCurrentController()
    own = controller.owner

    right_arrow = controller.sensors["right_arrow"]
    left_arrow = controller.sensors["left_arrow"]

    global GROUP_ID
    max = max_GROUP_ID - 2

    if right_arrow.positive and GROUP_ID <= max:
        #print("Right arrow has been pressed.")
        GROUP_ID = GROUP_ID + 1
        create_item_properties(groups[GROUP_ID])
        create_buttons()
        #print(GROUP_ID)
    if left_arrow.positive and GROUP_ID >= 1:
        #print("Left arrow has been pressed.")
        GROUP_ID = GROUP_ID - 1
        create_item_properties(groups[GROUP_ID])
        create_buttons()
        #print(GROUP_ID)

### LOAD - Load the external models from the 'models' subfolder inside the program
print("::LOAD::")

### Function that loads the models from the subfolders inside the program
def load_external_models(name):

    ### Finds all the 'blend' files in the 'models' subdirectory
    files = [f for f in os.listdir(models_directory + '/' + name) if 'blend' in f]
    #print("The files inside the folder",name,"are:",files)

    ### Load each found file
    for f in files:
        model = models_directory+name + '/' + f ### The file(s) in the "models" subfolder. "Name" is the name of the the subfolder. "f" is the filename of the blend file
        logic.LibLoad(model, 'Scene', load_actions = False, load_scripts = False, async = False) ### Load it with LibLoad (async messes up the loading)

print("Loading all the external models from their folders:")
for m in groups:
    print(" ", m)
    load_external_models(m)
print("Done.\n")

### This function is for debugging purposes
def show_loaded_models():
    logicList = bge.logic.LibList()
    print("The loaded models are:")
    for l in logicList:
        print(l)
    print("\n")
#show_loaded_models() ### This is commented out. IT's for debugging purposes only


### VARIABLES - Declaring the variables

### ID
ID = 0          ### Starting item (selects an item from the CSV array based on the item ID. 0 is the first item in the array list)
new_ID=0        ### Variable for the list index when a selection is made

### MODE - The snapping mode: 0 for free snap, 1 for center of object, 2 for 1/10ths of the object's face
global MODE
MODE = 1

### SCENE
scene = bge.logic.getCurrentScene()     ### The current scene
#print("The scene is:",scene)

ghost = scene.objects["ghost"]          ### The placeholder object. This will be the object that will move around the scene and hold the preview of the item. It is just an empty.
#print("The placeholder object is:",ghost)

preview = scene.objects["preview"]      ### The preview object (Suzanne the monkey). Will be replaced by the selected item's wireframe
#print("The preview object is:",preview)

### DATA - The object data (name, width, length, height) are imported from a CSV file. Creates the necessary lists for the item properties (name, dimensions etc).
print("::DATA::")

def create_item_properties(file):

    ListFile = data_directory+file+'.csv' ### The csv file to create the data from.
    #print("The file used to create the lists is:",ListFile)

    ### Declare the variables as global to be used by other modules in the program
    global items
    global wireframes
    global i_width
    global i_length
    global i_height

    with open(ListFile) as N:
        items = [row["NAME"] for row in DictReader(N)]
        print("Items in the list are:")
        for i in items:
            print(" ", i)

    wireframes = items ### This needs improvement

    with open(ListFile) as W:
        i_width = [row["WIDTH"] for row in DictReader(W)] ### i_width is item width
    with open(ListFile) as L:
        i_length = [row["LENGTH"] for row in DictReader(L)] ### i_length is item length
    with open(ListFile) as H:
        i_height = [row["HEIGHT"] for row in DictReader(H)] ### i_height is item height
    #print("Item property lists created.\n")

print("Creating the lists for the item properties...")
create_item_properties(groups[GROUP_ID]) ### This creates the item properties for the object group that is selected
print("Done.\n")

item = items[ID]                        ### Selected item from the CSV list.
#print("Item is",item)

wireframe = str(items[ID]+'w')          ### The wireframe version of the item (The name of the item + w at then)
#print("Wireframe is",wireframe)


### PREVIEW_MESH - Function to change the preview mesh to the currently selected. Runs constantly. Need to make it to change only once and stay like that (WIP)
def preview_mesh():

    controller = bge.logic.getCurrentController()
    #print("The controller is:",controller)
    own = controller.owner
    #print("Owner is:",own)

    ### Replace the default mesh (Suzanne, the monkey) with the item's wireframe
    own.replaceMesh(wireframe)


### DIMENSIONS - The wireframe item's dimensions (needs to be a floating number to work). This will be used to place items according to the object that the mouse is hovering over.
width = float(i_width[ID])
#print("Width is",width)
length = float(i_length[ID])
#print("Length is",length)
height = float(i_height[ID])
#print("Height is",height)

### MOUSE_OVER_BUTTON - The cursor status. If it's 1, the cursor is not over a button (and can place items on the grid). If it's 0, it cannot place new items until it goes back to 1.
mouse_is_over_button = 1

def mouse_over_button(): ### Function to disable the creation of new blocks when the mouse is over a button

    #print("Function to set the 'mouse_is_over_button' variable to 0 or 1")

    global mouse_is_over_button

    controller = bge.logic.getCurrentController()
    #print("The controller is:",controller)
    own = controller.owner
    #print("Owner is:",own)

    mouse_over_button = controller.sensors["mouse_over_button"]
    #print("Sensor is:",mouse_over_button)

    if mouse_over_button.positive:
        mouse_is_over_button = 0
        #print("Mouse is over",own,"\n")
        #print("Mouse is over a button. mouse_is_over_button is",mouse_is_over_button,". Owner is",own)
    if not mouse_over_button.positive:
        mouse_is_over_button = 1
        #print("Mouse is over a button. mouse_is_over_button is",mouse_is_over_button,". Owner is",own)

### Function to hide the bounding box object
def hide_bounding_box():

    controller = bge.logic.getCurrentController()
    own = controller.owner

    H = controller.sensors["H"]

    scene = bge.logic.getCurrentScene()

    visibility = own["visibility"]

    if H.positive and visibility == 0:
        for obj in scene.objects:
            if obj.name == "bounding_box":
                obj.visible = False
        own["visibility"] = 1
        print(own["visibility"])

    if H.positive and visibility == 1:
        for obj in scene.objects:
            if obj.name == "bounding_box":
                obj.visible = True
        own["visibility"] = 0
        print(own["visibility"])



## GET ID - Function to get the menu item's ID number (GUI scene). This will be used to change the item, the wireframe and the dimensions of the item.
def get_ID():

    ### VARIABLES - Define global variables to be used between scenes. The get_ID() function is used by the buttons on the different scenes

    ### First, set the variables as global
    global ID
    #print("Global ID is:",ID)
    global new_ID
    #print("Global new_ID is:",new_ID)
    global item
    #print("Global item is:",item)
    global wireframe
    #print("Global wireframe is:",wireframe)
    global width
    #print("Global width is:",width)
    global length
    #print("Global length is:",length)
    global height
    #print("Global height is:",height)

    controller = bge.logic.getCurrentController()
    #print("The controller is:",controller)
    own = controller.owner
    #print("The owner is:",own)
    scene = bge.logic.getCurrentScene()

    left_click_button = controller.sensors["left_click_button"]
    mouse_over_button = controller.sensors["mouse_over_button"]


    if mouse_over_button.positive and left_click_button.positive:
        ### Get the item's ID, which will be the new ID for everything
        global new_ID
        new_ID = own["ID"]
        #print("The new ID is:",new_ID)

        ### Then, set the new id to all the items
        item = items[new_ID]
        #print(item)
        wireframe = wireframes[new_ID]
        #print(wireframe)
        width = i_width[new_ID]
        #print("New width is:",width)
        length = i_length[new_ID]
        #print("New length is:",length)
        height = i_height[new_ID]
        #print("New height is:",height)

### GRIDS ###

### Add the first cube at 0,0,0
grid = scene.addObject('grid.000', ghost, 0)
grid.worldPosition = [0, 0, 0]

### GRID_PATTERNS - Different grid patterns that repeat.
# Format: grid_pattern = ([grid_name,x,y,z], [grid_name,x,y,z])
grid_pattern_001 = (
    ['grid.111', 0.0, 0.0, 0.0],
    ['grid.111', 1.0, 0.0, 0.0]
)
grid_pattern_002 = (
    ['grid.111', 0.0, 0.0, 0.0],
    ['grid.211', 1.5, 0.0, 0.0]
)
grid_pattern_003 = (
    ['grid.111', 0.0, 0.0, 0.0],
    ['grid.121', 0.0, 1.5, 0.0]
)
grid_pattern_004 = (
    ['grid.111', 0.0, 0.0, 0.0],
    ['grid.211', 1.5, 0.0, 0.0],
    ['grid.121', 0.0, 1.5, 0.0],
    ['grid.111', 1.0, 1.0, 0.0],
    ['grid.111', 2.0, 1.0, 0.0],
    ['grid.111', 2.0, 2.0, 0.0],
    ['grid.111', 1.0, 2.0, 0.0]
)
grid_pattern_005 = (
    ['grid.331', 0.0, 0.0, 0.0],
    ['grid.331', 3.0, 0.0, 0.0],
    ['grid.331', 0.0, 3.0, 0.0],
    ['grid.331', 3.0, 3.0, 0.0]
)
grid_pattern_006 = (
    ['grid.111', 0.0, 0.0, 0.0],
    ['grid.111', 1.0, 0.0, 0.1],
    ['grid.111', 1.0, 1.0, 0.2],
    ['grid.111', 0.0, 1.0, 0.3],
    ['grid.111', -1.0, 1.0, 0.2],
    ['grid.111', -1.0, 0.0, 0.1]
)

### CLEAR_GRID - Function to clear the current grid
def clear_grid():

    ### First, delete all the grid objects. ### Needs work
    object_list = [obj for obj in scene.objects]
    grid_objects = ['grid.000', 'grid.111', 'grid.211', 'grid.121', 'grid.221', 'grid.331'] ### Here I put all the grid blocks names
    for obj in object_list:
        if obj.name in grid_objects:
            #print("Grid object",obj,"is being removed")
            obj.endObject()

### CREATE_GRID - Function to create the grid
def generate_grid_pattern(rows,row_distance,columns,column_distance,pattern):

    print("Function is creating the grid pattern...")

    ### First clear the previous grids
    print("Clearing previous grid...")
    clear_grid()
    print("Done.")

    r = rows
    rd = row_distance
    c = columns
    cd = column_distance

    print("Creating the pattern...")

    n = -r                                                ### This will start the grid symmetrically to the Y Axis to the negative value.
    while n<r:
        m = -c                                            ### This will start the grid symmetrically to the X Axis to the negative value.
        while m < c:
            for i in pattern:
                #print(i)
                name = i[0]
                x = i[1] + rd * n                           ### This will place the grid object at the local position (pattern's X position) plus the distance it will repeat at, times n. ### TODO more explanation
                y = i[2] + cd * m                           ### This will place the grid object at the local position (pattern's Y position) plus the distance it will repeat at, times m. ### TODO more explanation
                z = i[3]                                ### This will place the grid object at the local position (pattern's Z position). Currently the system I created doesn't allow me to create grid patterns in the 3d space. Only 2d.
                ghost.worldPosition = [x, y, z]         ### This moves the ghost item to the new position, where it will replicate the grid object
                #print(ghost.worldPosition)
                obj = scene.addObject(name, ghost, 0)   ### This adds a grid object at the ghost's position
            m += 1
        n += 1

    print("Done.")


### SEND MESSAGE - Send a message to the main scene's camera.
def send_message():

    controller = bge.logic.getCurrentController()
    #print("Controller is:",controller)
    own = controller.owner
    #print("Owner is:",own)

    left_click_button = controller.sensors["left_click_button"]
    mouse_over_button = controller.sensors["mouse_over_button"]

    if mouse_over_button.positive and left_click_button.positive:

        ### SAVE/LOAD. 1-9
        if own["ID"] == 1:
            own.sendMessage("action", "save_data")
        if own["ID"] == 2:
            own.sendMessage("action", "load_data")

        ### GRIDS. 101-199
        if own["ID"] == 101:
            own.sendMessage("action", "generate_grid_1x1")
            #print("Message to create the grid is sent!")
        if own["ID"] == 102:
            own.sendMessage("action", "generate_grid_2x1")
            #print("Message to create the grid is sent!")
        if own["ID"] == 103:
            own.sendMessage("action", "generate_grid_1x2")
            #print("Message to create the grid is sent!")
        if own["ID"] == 104:
            own.sendMessage("action", "generate_grid_1x2x2")
            #print("Message to create the grid is sent!")
        if own["ID"] == 105:
            own.sendMessage("action", "generate_grid_3x3")
            #print("Message to create the grid is sent!")
        if own["ID"] == 106:
            own.sendMessage("action", "generate_grid_3d.001")
            #print("Message to create the grid is sent!")


def message_received():
    """Function for receiving a message. When a message is received (by the
    message sensor of the camera at the main scene), it reads the body of the
    message and acts accordingly.
    """
    controller = bge.logic.getCurrentController()
    #print("Controller is:",controller)
    own = controller.owner
    #print("Owner is:",own)

    message_sensor = controller.sensors["message_sensor"]
    #print(message_sensor)

    if message_sensor.positive:
        #print("Message_received")
        action = message_sensor.bodies[0] ### Reads the body of the message sent and acts accordingly

        ### SAVE AND LOAD
        if action == "save_data":
            #print("Saving the data")
            save_data()
        if action == "load_data":
            #print("Loading the data")
            load_data()

        ### GRIDS
        if action == "generate_grid_1x1":
            #print("Generating 1x1 grid pattern")
            generate_grid_pattern(6,2,12,1,grid_pattern_001)
        if action == "generate_grid_2x1":
            #print("Generating 2x1 grid pattern")
            generate_grid_pattern(4,3,12,1,grid_pattern_002)
        if action == "generate_grid_1x2":
            #print("Generating 1x2 grid pattern")
            generate_grid_pattern(12,1,4,3,grid_pattern_003)
        if action == "generate_grid_1x2x2":
            #print("Generating 1x2x2 grid pattern")
            generate_grid_pattern(4,3,4,3,grid_pattern_004)
        if action == "generate_grid_3x3":
            #print("Generating 3x3 grid pattern")
            generate_grid_pattern(3,6,3,6,grid_pattern_005)
        if action == "generate_grid_3d.001":
            #print("Generating 3x3 grid pattern")
            generate_grid_pattern(4,3,6,2,grid_pattern_006)


def create_building(CSVfile):
    """Function to create a building with instructions from a CSV file."""
    controller = bge.logic.getCurrentController()
    #print("Controller is:",controller)
    own = controller.owner
    #print("Owner is:",own)

    ### First, delete all the grid objects.
    clear_grid()

    DataFile = CSVfile ### The CSVfile is the file that holds the instructions
    ### Count the rows
    with open(DataFile,"r") as D:
        CSVreader = csv.reader(D,delimiter = ",")
        data = list(CSVreader)
        row_count = (len(data)-1)
        #print("There are ",row_count,"rows of data")

    ### Retrieve the data from the csv file and seperate them to item name, x location, y location, z location and rotation
    with open(DataFile) as D:
        items = [row["ITEM"] for row in DictReader(D)]
        #print(items)
    with open(DataFile) as X:
        locationX = [row["X"] for row in DictReader(X)]
        #print(locationX)
    with open(DataFile) as Y:
        locationY = [row["Y"] for row in DictReader(Y)]
        #print(locationY)
    with open(DataFile) as Z:
        locationZ = [row["Z"] for row in DictReader(Z)]
        #print(locationZ)
    with open(DataFile) as R:
        rotationR = [row["ROTATION"] for row in DictReader(R)]
        #print(rotationR)

    i=0 ### Start from the first row
    while i < row_count:
        #print("i is:",i)
        #print("Item is:",items[i]) ### This is used later
        #print("X position is:",locationX[i])
        x = float(locationX[i])
        #print("Y position is:",locationY[i])
        y = float(locationY[i])
        #print("Z position is:",locationZ[i])
        z = float(locationZ[i])
        #print("Rotation is:",rotationR[i])
        r = float(rotationR[i])
        #print(r)
        ghost.worldPosition = [x,y,z]
        #print(ghost.worldOrientation.to_euler().z)

        ### This one was tricky: rotate the empty according to the radian(?) values of the CSV file
        ### First, convert the local orientation to Euler
        xyz = ghost.localOrientation.to_euler()
        #print("Before the rotation. Z rotation is:",xyz[2])
        ### Then, change the Z value of the rotation to the one from the CSV file
        xyz[2] = r
        #print("After the rotation. Z rotation is:",xyz[2])
        ### Finally, change the empty's local orientation with the new Z value
        ghost.localOrientation = xyz.to_matrix()

        obj = scene.addObject(items[i], "ghost", 0)
        i = i+1


### SAVE / LOAD ###

def save_data():
    """Export the model's data (name,location) to a txt file."""
    print("Saving the data to the external file...")
    ### Get the list of scenes
    scenes = bge.logic.getSceneList()
    #print("List of scenes:",scenes)

    ### The file to save the values. Needs to be opened first.
    list_file = custom_directory + '/custom001.csv'
    list_file_open = open(list_file, 'w')
    #print("Opening list_file at",list_file)

    ### Iterate through the MAIN scene's objects
    for scene in scenes :
        if scene.name == "MAIN":
            #print("scene : %s"%scene.name)
            ### List of all the objects in the game
            object_list = [obj for obj in scene.objects]
            #print(object_list)
            ### Iterate through the objects and find it's values for name, x position, y position and z position
            excluded_objects = ['light','camera', 'preview', 'ghost', 'button']
            list_file_open.write("ITEM,X,Y,Z,ROTATION\n")
            for obj in object_list:
                name = str(obj.name) ### Strings are needed to be able to write in the txt file
                x = str(round(obj.worldPosition[0],2))
                y = str(round(obj.worldPosition[1],2))
                z = str(round(obj.worldPosition[2],2))
                r = str(round(obj.localOrientation.to_euler().z,3))
                #print(name,"'s rotation is:",r)

                ### Write the values to the file
                #print("Saving",name,"at",x,y,z,"to the file.")
                ### Save only the objects that don't have a name that begins with the 'excluded_objects' list (leaving out the default scene items (camera, lights etc))
                if not any(excluded_objects in name for excluded_objects in excluded_objects):
                #if not name.startswith('grid'):
                    list_file_open.write(name+","+x+","+y+","+z+","+r+"\n")
                    #print(name)

    list_file_open.close()
    print("Data exported. Closing the open list file.")
    print("Done.\n")


def load_data():
    print("Loading the data from the external file...")
    create_building(custom_directory+'/custom001.csv')
    print("Done.\n")


def create_buttons():
    """Function to create the buttons. Replaces the cube mesh with the mesh from the loaded object."""
    print("Creating the buttons...")

    number_of_items = len(items)
    print("There are",number_of_items,"items in this list.")

    mesh_button = ["button.placeholder."+str("{0:0=3d}".format(o)) for o in range(0,number_of_items)] ### "{0:0=3d}".format(o) <== This means to format the numbers to 3 decimal one. For example, write 3 as 003

    print("Mesh buttons to be replaced are:")
    for i in range(0,number_of_items):
        obj = scene.objects[mesh_button[i]]
        print(obj)
        button_ID = obj["ID"]
        #print("Mesh button's ID is:",button_ID)
        obj.replaceMesh(items[button_ID])

    print("Done.\n")


### INFO_TEXT - Dynamically loaded info text (from txt file)

info_files = [f for f in os.listdir(info_directory) if 'txt' in f]
print("Info files inside the info folder are:",info_files)

def show_info_text():

    controller = bge.logic.getCurrentController()
    #print("The controller is:",controller)
    own = controller.owner
    #print("The owner is:",own)

    scene = bge.logic.getCurrentScene()
    #print("Current scene is:",scene)

    message_sensor = own.sensors["update_text"]

    if message_sensor.positive:
        print("Message received. Updating text.")

        info_file = info_files[GROUP_ID]
        print("Selected file is:",info_file,"\n")
        info_txt = info_directory+info_file
        print("Info file path is:",info_txt)
        print("Opening info file for reading..")
        info_txt_open = open(info_txt, 'r')
        print("Done.\n")
        dynamic_text = scene.objects["info_text"]
        info_text_wrapped = textwrap.wrap(info_txt_open.read(),160)
        #print(info_text_wrapped)
        dynamic_text.text = '\n'.join([l for l in info_text_wrapped])
        info_txt_open.close()


### WIKIPEDIA - Function to open wikipedia link in the web browser
def open_wikipedia_link():

    controller = bge.logic.getCurrentController()
    #print("The controller is:",controller)
    own = controller.owner
    #print("The owner is:",own)

    scene = bge.logic.getCurrentScene()
    #print("Current scene is:",scene)

    mouse_over_button = own.sensors["mouse_over_button"]
    left_click_button = own.sensors["left_click_button"]

    if mouse_over_button.positive and left_click_button.positive:
        print("Wikipedia button has been pressed. Opening the website.")
        info_file = info_files[GROUP_ID]
        print("Selected file is:",info_file,"\n")
        info_txt = info_directory+info_file
        print("Info file path is:",info_txt)
        print("Opening info file for reading..")
        info_txt_open = open(info_txt, 'r')
        print("Done.\n")
        url = info_txt_open.readline()

        webbrowser.open(url)


### Fix text resolution. Default resolution is 1.0 (72dpi).
def fix_text_resolution():

    scene = bge.logic.getCurrentScene()

    #print("Text starting resolution is:",scene.objects["info_text"].resolution)
    scene.objects["info_text"].resolution = 32.0
    #print("Text changed resolution is:",scene.objects["info_text"].resolution)


### CAMERA_POSITION - Set the camera's position
def set_camera_position():

    controller = bge.logic.getCurrentController()
    own = controller.owner

    #print(own.worldOrientation)

    ### Setup the sensors
    Num1 = controller.sensors["Num1"]
    Num2 = controller.sensors["Num2"]
    Num3 = controller.sensors["Num3"]
    Num4 = controller.sensors["Num4"]
    Num5 = controller.sensors["Num5"]
    Num6 = controller.sensors["Num6"]
    Num7 = controller.sensors["Num7"]
    Num8 = controller.sensors["Num8"]
    Num9 = controller.sensors["Num9"]

    ### Setup the conditions for the camera position and orientation
    # SW (southwest)
    if Num1.positive:
        print("Seting the camera to the SOUTHWEST position.")
        own.worldPosition = [-32.0, -32.0, 44.0]
        own.worldOrientation = [
            [0.7071, 0.5000, -0.5000],
            [-0.7071, 0.5000, -0.5000],
            [-0.0000, 0.7071,  0.7071]
        ]
    # S (south)
    if Num2.positive:
        print("Seting the camera to the SOUTH position.")
        own.worldPosition = [0.0, -44.0, 44.0]
        own.worldOrientation = [
            [1.0000, 0.0000,  0.0000],
            [0.0000, 0.7071, -0.7071],
            [-0.0000, 0.7071,  0.7071]
        ]
    # S (south)
    if Num3.positive:
        print("Seting the camera to the SOUTHEAST position.")
        own.worldPosition = [32.0, -32.0, 44.0]
        own.worldOrientation = [
            [0.7071, -0.5000,  0.5000],
            [0.7071,  0.5000, -0.5000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # W (west)
    if Num4.positive:
        print("Seting the camera to the WEST position.")
        own.worldPosition = [-44.0, -0.0, 44.0]
        own.worldOrientation = [
            [-0.0000,  0.7071, -0.7071],
            [-1.0000, -0.0000,  0.0000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # O (Original position)
    if Num5.positive:
        print("Reseting the camera to its original position.")
        own.worldPosition = [32.0, -32.0, 44.0]
        own.worldOrientation = [
            [0.7071, -0.5000,  0.5000],
            [0.7071,  0.5000, -0.5000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # E (east)
    if Num6.positive:
        print("Seting the camera to the EAST position.")
        own.worldPosition = [44.0, 0.0, 44.0]
        own.worldOrientation = [
            [0.0000, -0.7071,  0.7071],
            [1.0000,  0.0000, -0.0000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # NW (northwest)
    if Num7.positive:
        print("Seting the camera to the NORTHWEST position.")
        own.worldPosition = [-32.0, 32.0, 44.0]
        own.worldOrientation = [
            [-0.7071,  0.5000, -0.5000],
            [-0.7071, -0.5000,  0.5000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # N (north)
    if Num8.positive:
        print("Seting the camera to the NORTH position.")
        own.worldPosition = [0.0, 44.0, 44.0]
        own.worldOrientation = [
            [-1.0000, -0.0000, 0.0000],
            [0.0000, -0.7071, 0.7071],
            [-0.0000,  0.7071, 0.7071]
        ]
    # NE (northeast)
    if Num9.positive:
        print("Seting the camera to the NORTHEAST position.")
        own.worldPosition = [32.0, 32.0, 44.0]
        own.worldOrientation = [
            [-0.7071, -0.5000, 0.5000],
            [0.7071, -0.5000, 0.5000],
            [-0.0000,  0.7071, 0.7071]
        ]


def take_screenshot():
    """Function to take a screenshot. Requires Imagemagick in Linux. Windows support is TODO"""
    controller = bge.logic.getCurrentController()
    #print("The controller is:",controller)
    own = controller.owner
    #print("The owner is:",own)

    scene = bge.logic.getCurrentScene()
    #print("Current scene is:",scene)

    mouse_over_button = own.sensors["mouse_over_button"]
    left_click_button = own.sensors["left_click_button"]

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

    if mouse_over_button.positive and left_click_button.positive:
        print("Taking screenshot...")
        subprocess.run(screenshot_args)


### PHASE 2: MAIN ###

### MAIN - The main function (MAIN scene) that controls everything.
def main():

    controller = bge.logic.getCurrentController()
    #print("The controller is:",controller)
    own = controller.owner
    #print("Owner is:",own)

    ### The Sensors (attached to MAIN scene's camera). Left click, Right Click and Mouse Over
    left_click = controller.sensors["left_click"]
    right_click = controller.sensors["right_click"]
    mouse_over = controller.sensors["mouse_over"]
    ### Snapping mode sensors: 1 for center of face, 2 for 1/10th of face's potision, 3 for free snap
    mode_1 = controller.sensors["mode_1"]
    mode_2 = controller.sensors["mode_2"]
    mode_3 = controller.sensors["mode_3"]

    global MODE

    if mode_1.positive:
        #print("Mode 1 is active. Snapping to center of face.")
        MODE = 1
        #print("Mode is:",MODE)
    if mode_2.positive:
        #print("Mode 2 is active. Snapping to 1/10th of face's position.")
        MODE = 2
        #print("Mode is:",MODE)
    if mode_3.positive:
        #print("Mode 3 is active. Snapping freely on the face.")
        MODE = 3
        #print("Mode is:",MODE)

    ### The preview's position is the same as the ghost's position. Updates constantly.
    preview.position = ghost.position
    ### Same for the orientation (rotation)
    preview.worldOrientation = ghost.worldOrientation

    ### MOUSE_OVER - The "mouse over" function
    if mouse_over.positive and mouse_is_over_button == 1:

        #print("The mouse is over a button.")

        ### Get the object that the ray hit
        rayObj = mouse_over.hitObject
        #print("The object hit by the ray is:",rayObj)
        #print("Ray object's world position is:",rayObj.worldPosition)
        #rayObj_width = [i[1] for i in merged_item_property_list if str(rayObj) in i[0]]
        #print("Item's width is:",rayObj_width)
        #rayObj_length = [i[2] for i in merged_item_property_list if str(rayObj) in i[0]]
        #print("Item's length is:",rayObj_length)
        #rayObj_height = [i[3] for i in merged_item_property_list if str(rayObj) in i[0]]
        #print("Item's height is:",rayObj_height)

        #for i in merged_item_property_list:
        #    if str(rayObj) in i[0]:
        #        item_width = i[1]
        #        item_length = i[2]
        #        item_height = i[3]

        ### Get the object's normal face
        rayNormal = mouse_over.hitNormal
        #print("The object normal is:",rayNormal)
        print(" rayNormal[0] is:",rayNormal[0],"\n","rayNormal[1] is:",rayNormal[1],"\n","rayNormal[2] is:",rayNormal[2],"\n",)

        ### Get the ray's position
        rayPos = mouse_over.hitPosition
        #print("The ray's position is: ",rayPos)
        #print("The ray's X position is: ",rayPos[0])
        #print("The ray's Y position is: ",rayPos[1])
        #print("The ray's Z position is: ",rayPos[2])
        #print("\n")

        #print(rayObj.worldOrientation)

        ### PLACE - Place the ghost object on the side of the object the mouse is over of, according to the object's dimensions.

        ### x axis
        ### positive
        if round(rayNormal[0],2) == 1:
            if MODE == 1:
                ghost.worldPosition = [rayPos[0] + float(length)/2, rayObj.worldPosition.y, rayObj.worldPosition.z]
            if MODE == 2:
                ghost.worldPosition = [rayPos[0] + float(length)/2, round(rayPos[1],1), round(rayPos[2],1)]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0] + float(length)/2, rayPos[1], rayPos[2]]
        ### negative
        if rayNormal[0] == -1:
            if MODE == 1:
                ghost.worldPosition = [rayPos[0] - float(length)/2, rayObj.worldPosition.y, rayObj.worldPosition.z]
            if MODE == 2:
                ghost.worldPosition = [rayPos[0] - float(length)/2, round(rayPos[1],1), round(rayPos[2],1)]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0] - float(length)/2, rayPos[1], rayPos[2]]

        ### y axis
        ### positive
        if rayNormal[1] == 1:
            if MODE == 1:
                ghost.worldPosition = [rayObj.worldPosition.x, rayPos[1] + float(width)/2, rayObj.worldPosition.z]
            if MODE == 2:
                ghost.worldPosition = [round(rayPos[0],1), rayPos[1] + float(width)/2, round(rayPos[2],1)]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0], rayPos[1] + float(width)/2, rayPos[2]]
        ### negative
        if rayNormal[1] == -1:
            if MODE == 1:
                ghost.worldPosition = [rayObj.worldPosition.x, rayPos[1] - float(width)/2, rayObj.worldPosition.z]
            if MODE == 2:
                ghost.worldPosition = [round(rayPos[0],1), rayPos[1] - float(width)/2, round(rayPos[2],1)]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0], rayPos[1] - float(width)/2, rayPos[2]]

        ### z axis
        ### positive
        if rayNormal[2] == 1:
            if MODE == 1:
                ghost.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayPos[2] + float(height)/2]
            if MODE == 2:
                ghost.worldPosition = [round(rayPos[0],1), round(rayPos[1],1), rayPos[2] + float(height)/2]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0], rayPos[1], rayPos[2] + float(height)/2]
        ### negative
        if rayNormal[2] == -1:
            if MODE == 1:
                ghost.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayPos[2] - float(height)/2]
            if MODE == 2:
                ghost.worldPosition = [round(rayPos[0],1), round(rayPos[1],1), rayPos[2] - float(height)/2]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0], rayPos[1], rayPos[2] - float(height)/2]

        ### ADD and DELETE ###

        ### ADD - Add object when you left click
        if left_click.positive and mouse_is_over_button == 1:

            #print("Left mouse button has been clicked.")

            ### Adds an object (item) at the position of the ghost (ghost) at the frame 0 ### Maybe I can use the frames to do the UNDO function. TODO
            obj = scene.addObject(item, ghost, 0)
            bbox = scene.addObject("bounding_box", ghost, 0)

            #bbox.worldScale = (float(length), float(width), float(height))

            ### LOCATION - Location of the newly added object (same as the ghost's position)
            obj.worldPosition = ghost.worldPosition
            bbox.worldPosition = ghost.worldPosition
            ### ROTATION - Orientation of the new object (same as the ghost's rotation)
            obj.worldOrientation = ghost.worldOrientation
            bbox.worldOrientation = ghost.worldOrientation

        ### DELETE - Delete object
        if right_click.positive:
            rayObj.endObject()



### NOTES ### NOTES ### NOTES ### NOTES ### NOTES ###

# EULER                             #
# Euler's rotation is as follows:   #
#     0 degrees   =   0.0           #
#    90 degrees   =   1.57          #
#   180 degrees   =  -3.14          #
#   270 degrees   =  -1.57          #
#               (these are radians) #

### message_sensor.positive is used because the logic brick sends two pulses
### instead of one (one for positive and one for negative) and so it executes
### the functiions twice. I need to tell the program to execute the function
### only when the positive pulse is sent.
