# PHASE 0: IMPORT - Importing the necessary modules
import bge  # bge - The Blender Game Engine Python library
import csv  # csv - The CSV Library for parsing the csv files
import math  # math
import mathutils  # mathutils
import os  # os - Used to find the path names
import subprocess  # subprocess - Executes system functions. Used mainly for the screenshots with Imagemagick.
import textwrap  # textwrap - Text wrapper (for the info section)
import time  # time - Needed for the date/time format at the screenshots.
import webbrowser  # webbrowser - Opens a web browser (will be used to open wikipedia pages)
from bge import logic  # logic - Needed to load external the files
from csv import DictReader  # DictReader - DictReader is needed to read the csv file's columns
from config import *

# PHASE 1: INITIALIZATION
print("\n\n\n:::INITIALIZATION:::\nInitializing the main script...\n\n:::PHASE 1:::")


# DEBUGGING
DEBUG=False
print("(Debugging is set to", DEBUG, ")\n")
def debug_print(*args):
    """Function that set the debugging mode On (True) or Off (False)"""
    if DEBUG:
        print(*args)


# GROUP
# The group at which the object(s) belong. The grouping is sorted
# by the folders in the "models" subfolder.
print("::GROUPS::\nCreating the object groups...")
groups = [g for g in os.listdir(models_dir)]  # Get a list of all the subfolders in the "models" folder
max_GROUP_ID = len(groups)  # Get the maximum number of subfolders
debug_print("There are", max_GROUP_ID, "groups of models.")
GROUP_ID=0  # An "id" variable to select the different groups
debug_print("The groups are:")
for g in groups:
    debug_print(" ", g)
debug_print("The active group is:", groups[GROUP_ID])
print("Done.\n")


def change_group():
    """Function to change the group of items.
    Used for switching between the sets of parts.
    Each group is made from the blend files inside the
    models folder.
    Use Left and Right keyboard arrows to change set.
    """

    controller = bge.logic.getCurrentController()
    own = controller.owner

    right_arrow = controller.sensors["right_arrow"]
    left_arrow = controller.sensors["left_arrow"]

    global GROUP_ID  # Make this global so it can be used by other modules
    max = max_GROUP_ID - 2

    if right_arrow.positive and GROUP_ID <= max:
        debug_print("Right arrow has been pressed.")
        GROUP_ID = GROUP_ID + 1
        create_item_properties(groups[GROUP_ID])
        create_buttons()
        debug_print(GROUP_ID)

    if left_arrow.positive and GROUP_ID >= 1:
        debug_print("Left arrow has been pressed.")
        GROUP_ID = GROUP_ID - 1
        create_item_properties(groups[GROUP_ID])
        create_buttons()
        debug_print(GROUP_ID)


# LOAD
# Load the external models from the 'models' subfolder inside the program.
print("::LOAD::")


def load_external_models(name):
    """Function that loads the models from the subfolders
    inside the program. It finds all the 'blend' files in the
    'models' subdirectory and loads them in the program
    """

    files = [f for f in os.listdir(models_dir + '/' + name) if 'blend' in f]
    debug_print("The files inside the folder {} are: ".format(name, files))

    for f in files:
        """The file(s) in the "models" directory.
        'Name' is the subfolder in the directory.
        'f' is the filename of the blend file.
        """
        model = models_dir+name + '/' + f
        """Load it with LibLoad. 'async' messes up the loading,
        so leave it to False.
        """
        logic.LibLoad(model, 'Scene', load_actions = False, load_scripts = False, async = False)


print("Loading all the external models from their folders:")
for m in groups:
    debug_print(" ", m)
    load_external_models(m)
print("Done.\n")


def show_loaded_models():
    """This function is for debugging purposes only."""
    logicList = bge.logic.LibList()
    print("The loaded models are:")
    for l in logicList:
        print(l)
    print("\n")

if DEBUG:
    show_loaded_models()


# VARIABLES - ID and NEW_ID
# Declaring the variables.
#
# ID is the starting item's ID (game property).
# The program will set the active item as the one with the corresponding ID,
# selected from the CSV file. 0 is the first item in the array list.
#
# NEW_ID is used when a different item is selected.
ID = 0
new_ID=0


# VARIABLES - MODE
# This is the snapping mode (how the objects snap to eachother).
#
# MODE 1 is for center of object.
# MODE 2 for 1/10ths of the object's face.
# MODE 3 is for free snap.
#
# Declaring the variable as global because it will be used later
# by the function that changes snapping modes.
global MODE
MODE = 1


# VARIABLES - scene, ghost, preview
#
# 'scene' is the current scene
#
# 'ghost' is the placeholder object. This will be the object
# that will move around the scene and hold
# the preview of the item. It is just an empty.
#
# 'preview' is the preview object (Suzanne the monkey at first). This
# will be replaced by the selected item's wireframe.
scene = bge.logic.getCurrentScene()
ghost = scene.objects["ghost"]
preview = scene.objects["preview"]


# "DATA
# The object data (name, width, length, height) are imported
# from a CSV file. Creates the necessary lists for the item
# properties (name, dimensions etc).
print("::DATA::")

def create_item_properties(file):
    """Function to create the lists with the items'
    properties (name, width, length, height).
    """
    ListFile = data_dir+file+'.csv'  # The csv file to create the data from.
    debug_print("The file used to create the lists is:", ListFile)

    """Declare the variables as global so that they
    can be used by other modules in the program.
    """
    global items
    global wireframes
    global i_width
    global i_length
    global i_height

    with open(ListFile) as N:
        items = [row["NAME"] for row in DictReader(N)]
        debug_print("Items in the list are:")
        for i in items:
            debug_print(" ", i)

    wireframes = items  # This needs improvement

    with open(ListFile) as W:
        i_width = [row["WIDTH"] for row in DictReader(W)]
    with open(ListFile) as L:
        i_length = [row["LENGTH"] for row in DictReader(L)]
    with open(ListFile) as H:
        i_height = [row["HEIGHT"] for row in DictReader(H)]
    debug_print("Item property lists created.\n")


# This creates the item properties for the selected group of objects.
# First time this runs it has GROUP_ID = 0
print("Creating the lists for the item properties...")
create_item_properties(groups[GROUP_ID])
print("Done.\n")


# VARIABLES - item, wireframe
#
# 'item' is the one with the selected ID
# from the 'items' list created from the CSV
#
# 'wireframe' is the same as the item name,
# but with a 'w' at the end (this is currently not
# implemented. it's for an older version)
item = items[ID]
wireframe = str(items[ID]+'w')  # Not implemented currently
debug_print("Item is", item, ". Wireframe is", wireframe)


# PREVIEW_MESH
def preview_mesh():
    """Function to change the preview mesh to the currently selected."""

    controller = bge.logic.getCurrentController()
    own = controller.owner

    own.replaceMesh(wireframe)


# DIMENSIONS
# The wireframe item's dimensions. The new items
# will be placed wherever the preview object is.
# Needs to be a floating number to work.
width = float(i_width[ID])
length = float(i_length[ID])
height = float(i_height[ID])
debug_print("Width is", width, ". \nLength is", length, ". \nHeight is", height)


# MOUSE_OVER_BUTTON
# The cursor status.
#
# If it's 1, the cursor is not over a button
# (and the user can place items on the grid).
#
# If it's 0, it cannot place new items,
# until it goes back to 1.
mouse_is_over_button = 1


def mouse_over_button():
    """Function to disable the creation of new blocks when the mouse
    is over a button.
    """
    debug_print("Function to set the 'mouse_is_over_button' variable to 0 or 1")

    global mouse_is_over_button  # This is global because it is used by objects in a different scene

    controller = bge.logic.getCurrentController()
    own = controller.owner

    mouse_over_button = controller.sensors["mouse_over_button"]

    if mouse_over_button.positive:
        mouse_is_over_button = 0
        debug_print("Mouse is over a button. mouse_is_over_button is", mouse_is_over_button, ". Owner is", own)

    if not mouse_over_button.positive:
        mouse_is_over_button = 1
        debug_print("Mouse is over a button. mouse_is_over_button is", mouse_is_over_button, ". Owner is", own)


#GET ID
def get_ID():
    """Function to get the menu item's ID number (GUI scene).
    This is used to change the item, the wireframe and the dimensions
    of the item.

    VARIABLES
    Define global variables to be used between scenes.
    The get_ID() function is used by the buttons on the different scenes.
    """
    global ID
    global new_ID
    global item
    global wireframe
    global width
    global length
    global height

    debug_print("ID is:", ID,
          "\nnew_ID is:", new_ID,
          "\nitem is:", item,
          "\nwireframe is:", wireframe,
          "\nwidth is:", width,
          "\nlength is:", length,
          "\nheight is:", height,
          "\n")

    controller = bge.logic.getCurrentController()
    own = controller.owner

    left_click_button = controller.sensors["left_click_button"]
    mouse_over_button = controller.sensors["mouse_over_button"]

    if mouse_over_button.positive and left_click_button.positive:
        """Set the new ID as the placeholder object's ID.
        Then, update all the values from the new object's properties.
        """
        new_ID = own["ID"]

        item = items[new_ID]
        wireframe = wireframes[new_ID]
        width = i_width[new_ID]
        length = i_length[new_ID]
        height = i_height[new_ID]

        debug_print("ID is:", ID,
              "\nnew_ID is:", new_ID,
              "\nSelected item is:", item,
              "\nSelected wireframe is:", wireframe,
              "\nSelected item's width is:", width,
              "\nSelected item's length is:", length,
              "\nSelected item's height is:", height,
              "\n")


# GRIDS
# Creates the grids when the buttons are pressed.
# First, add the first grid cube at x,y,z 0,0,0
grid = scene.addObject('grid.000', ghost, 0)
grid.worldPosition = [0, 0, 0]


# GRID_PATTERNS
# Different grid patterns that repeat themselves.
# The format is:
# grid_pattern = ([grid_name,x,y,z], [grid_name,x,y,z])
# TODO: create and save grid patterns (hard)
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


# CLEAR_GRID
def clear_grid():
    """Function to clear the current grid.
    Used before creating the new grid.

    First, delete all the grid objects.

    (The code needs a rewrite so as to include
    all the objects that have 'grid' in their name.
    Maybe write it with 'if any'? TODO)
    """
    object_list = [obj for obj in scene.objects]
    grid_objects = ['grid.000', 'grid.111', 'grid.211', 'grid.121', 'grid.221', 'grid.331'] ### Here I put all the grid blocks names
    for obj in object_list:
        if obj.name in grid_objects:
            debug_print("Grid object", obj, "is being removed")
            obj.endObject()

# CREATE_GRID
def generate_grid_pattern(rows, row_distance, columns, column_distance, pattern):
    """Function to create the grid.
    First clears the previous grids, then creates the new grid.
    """
    debug_print("Function is creating the grid pattern...")

    debug_print("Clearing previous grid...")
    clear_grid()
    debug_print("Done.")

    r = rows
    rd = row_distance
    c = columns
    cd = column_distance

    debug_print("Creating the pattern...")

    n = -r  # This will start the grid symmetrically to the Y Axis to the negative value.
    while n<r:
        m = -c  # This will start the grid symmetrically to the X Axis to the negative value.
        while m < c:
            for i in pattern:
                debug_print(i)
                name = i[0]
                x = i[1] + rd * n  # This will place the grid object at the local position (pattern's X position) plus the distance it will repeat at, times n. ### TODO more explanation
                y = i[2] + cd * m  # This will place the grid object at the local position (pattern's Y position) plus the distance it will repeat at, times m. ### TODO more explanation
                z = i[3]  # This will place the grid object at the local position (pattern's Z position). Currently the system I created doesn't allow me to create grid patterns in the 3d space. Only 2d.
                ghost.worldPosition = [x, y, z]  # This moves the ghost item to the new position, where it will replicate the grid object
                debug_print(ghost.worldPosition)
                obj = scene.addObject(name, ghost, 0)  # This adds a grid object at the ghost's position
            m += 1
        n += 1

    debug_print("Done.")


# SEND MESSAGE
def send_message():
    """Function to send a message to the message_listener empty."""
    controller = bge.logic.getCurrentController()
    own = controller.owner

    left_click_button = controller.sensors["left_click_button"]
    mouse_over_button = controller.sensors["mouse_over_button"]

    if mouse_over_button.positive and left_click_button.positive:

        # SAVE/LOAD. IDs: 1-9
        if own["ID"] == 1:
            own.sendMessage("action", "save_data")
        if own["ID"] == 2:
            own.sendMessage("action", "load_data")

        # GRIDS. IDs: 101-199
        if own["ID"] == 101:
            own.sendMessage("action", "generate_grid_1x1")
            debug_print("Message to create the grid is sent!")
        if own["ID"] == 102:
            own.sendMessage("action", "generate_grid_2x1")
            debug_print("Message to create the grid is sent!")
        if own["ID"] == 103:
            own.sendMessage("action", "generate_grid_1x2")
            debug_print("Message to create the grid is sent!")
        if own["ID"] == 104:
            own.sendMessage("action", "generate_grid_1x2x2")
            debug_print("Message to create the grid is sent!")
        if own["ID"] == 105:
            own.sendMessage("action", "generate_grid_3x3")
            debug_print("Message to create the grid is sent!")
        if own["ID"] == 106:
            own.sendMessage("action", "generate_grid_3d.001")
            debug_print("Message to create the grid is sent!")


# RECEIVE MESSAGE
def message_received():
    """Function for receiving a message. When a message is received (by the
    message_listener empty), it reads the body of the message and acts accordingly.
    """
    controller = bge.logic.getCurrentController()
    own = controller.owner

    message_sensor = controller.sensors["message_sensor"]

    if message_sensor.positive:
        debug_print("Message_received")
        action = message_sensor.bodies[0]  # Reads the body of the message sent and acts accordingly

        # SAVE AND LOAD
        if action == "save_data":
            debug_print("Saving the data")
            save_data()
        if action == "load_data":
            debug_print("Loading the data")
            load_data()

        # GRIDS
        if action == "generate_grid_1x1":
            debug_print("Generating 1x1 grid pattern")
            generate_grid_pattern(6, 2, 12, 1, grid_pattern_001)
        if action == "generate_grid_2x1":
            debug_print("Generating 2x1 grid pattern")
            generate_grid_pattern(4, 3, 12, 1, grid_pattern_002)
        if action == "generate_grid_1x2":
            debug_print("Generating 1x2 grid pattern")
            generate_grid_pattern(12, 1, 4, 3, grid_pattern_003)
        if action == "generate_grid_1x2x2":
            debug_print("Generating 1x2x2 grid pattern")
            generate_grid_pattern(4, 3, 4, 3, grid_pattern_004)
        if action == "generate_grid_3x3":
            debug_print("Generating 3x3 grid pattern")
            generate_grid_pattern(3, 6, 3, 6, grid_pattern_005)
        if action == "generate_grid_3d.001":
            debug_print("Generating 3x3 grid pattern")
            generate_grid_pattern(4, 3, 6, 2, grid_pattern_006)


# CREATE_BUILDING
def create_building(CSVfile):
    """Function to create a building from CSV file.
    First, deletes all the grid objects.
    """
    controller = bge.logic.getCurrentController()
    own = controller.owner

    clear_grid()

    DataFile = CSVfile  # The CSVfile that holds the instructions

    with open(DataFile, "r") as D:
        CSVreader = csv.reader(D, delimiter = ",")
        data = list(CSVreader)
        row_count = (len(data)-1) # Count the rows
        debug_print("There are ", row_count, "rows of data")

    # Retrieve the data from the csv file and seperate them
    # to item name, x location, y location, z location and rotation.
    with open(DataFile) as D:
        items = [row["ITEM"] for row in DictReader(D)]
    with open(DataFile) as X:
        locationX = [row["X"] for row in DictReader(X)]
    with open(DataFile) as Y:
        locationY = [row["Y"] for row in DictReader(Y)]
    with open(DataFile) as Z:
        locationZ = [row["Z"] for row in DictReader(Z)]
    with open(DataFile) as R:
        rotationR = [row["ROTATION"] for row in DictReader(R)]

    i=0  # Start from the first row
    while i < row_count:
        x = float(locationX[i])
        y = float(locationY[i])
        z = float(locationZ[i])
        r = float(rotationR[i])
        debug_print ("Item", i, "is:", items[i],
               "\nItem", i, "'s X position is:", locationX[i],
               "\nItem", i, "'s Y position is:", locationY[i],
               "\nItem", i, "'s Z position is:", locationZ[i],
               "\nItem", i, "'s Rotation is:", rotationR[i],
               "\n")
        ghost.worldPosition = [x, y, z]
        debug_print(ghost.worldOrientation.to_euler().z)

        # This one was tricky: rotate the empty according to the
        # radian(?) values of the CSV file.
        # First, convert the local orientation to Euler.
        xyz = ghost.localOrientation.to_euler()
        debug_print("Before the rotation. Z rotation is:", xyz[2])
        # Then, change the Z value of the rotation
        # to the one from the CSV file.
        xyz[2] = r
        debug_print("After the rotation. Z rotation is:", xyz[2])
        # Finally, change the empty's local orientation
        # with the new Z value.
        ghost.localOrientation = xyz.to_matrix()

        obj = scene.addObject(items[i], "ghost", 0)
        i = i+1

# SAVE DATA
def save_data():
    """Export the model's objects (name,location) to a csv file."""
    debug_print("Saving the data to the external file...")
    # Get the list of scenes
    scenes = bge.logic.getSceneList()
    debug_print("List of scenes:", scenes)

    # The file to save the values. Needs to be opened first.
    list_file = custom_dir + '/custom001.csv'
    list_file_open = open(list_file, 'w')
    debug_print("Opening list_file at", list_file)

    # Iterate through the MAIN scene's objects
    for scene in scenes :
        if scene.name == "MAIN":
            debug_print("scene : %s"%scene.name)
            # List of all the objects in the game
            object_list = [obj for obj in scene.objects]
            debug_print(object_list)
            # Iterate through the objects and find it's values for
            # name, x position, y position and z position
            excluded_objects = ['light', 'camera', 'preview', 'ghost', 'button']
            list_file_open.write("ITEM,X,Y,Z,ROTATION\n")
            for obj in object_list:
                name = str(obj.name) ### Strings are needed to be able to write in the txt file
                x = str(round(obj.worldPosition[0], 2))
                y = str(round(obj.worldPosition[1], 2))
                z = str(round(obj.worldPosition[2], 2))
                r = str(round(obj.localOrientation.to_euler().z, 3))
                debug_print(name, "'s rotation is:", r)

                # Write the values to the file
                debug_print("Saving", name, "at", x, y, z, "to the file.")
                # Save only the objects that don't have a name that
                # begins with the 'excluded_objects' list
                # (the default scene items like the camera, the lights etc)
                if not any(excluded_objects in name for excluded_objects in excluded_objects):
                    list_file_open.write(name+","+x+","+y+","+z+","+r+"\n")
                    debug_print(name)

    list_file_open.close()
    debug_print("Data exported. Closing the open list file.")
    debug_print("Done.\n")

# LOAD DATA
def load_data():
    """Function to load the data from the external file."""
    debug_print("Loading the data from the external file...")
    create_building(custom_dir+'/custom001.csv')
    debug_print("Done.\n")


def create_buttons():
    """Function to create the buttons. Replaces the cube mesh with the mesh from the loaded object."""
    debug_print("Creating the buttons...")

    number_of_items = len(items)
    debug_print("There are", number_of_items, "items in this list.")

    mesh_button = ["button.placeholder."+str("{0:0=3d}".format(o)) for o in range(0, number_of_items)] ### "{0:0=3d}".format(o) <== This means to format the numbers to 3 decimal one. For example, write 3 as 003

    debug_print("Mesh buttons to be replaced are:")
    for i in range(0, number_of_items):
        obj = scene.objects[mesh_button[i]]
        debug_print(obj)
        button_ID = obj["ID"]
        debug_print("Mesh button's ID is:", button_ID)
        obj.replaceMesh(items[button_ID])

    debug_print("Done.\n")


# INFO_TEXT
# Dynamically loaded info text (from txt file)
info_files = [f for f in os.listdir(info_dir) if 'txt' in f]
debug_print("Info files inside the info folder are:", info_files)


def show_info_text():
    """Function that shows the text in the txt files."""
    controller = bge.logic.getCurrentController()
    own = controller.owner

    scene = bge.logic.getCurrentScene()

    message_sensor = own.sensors["update_text"]

    if message_sensor.positive:
        debug_print("Message received. Updating text.")
        info_file = info_files[GROUP_ID]
        debug_print("Selected file is:", info_file, "\n")
        info_txt = info_dir+info_file
        debug_print("Info file path is:", info_txt)
        debug_print("Opening info file for reading..")
        info_txt_open = open(info_txt, 'r')
        debug_print("Done.\n")
        dynamic_text = scene.objects["info_text"]
        info_text_wrapped = textwrap.wrap(info_txt_open.read(), 160)
        debug_print(info_text_wrapped)
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
        debug_print("Wikipedia button has been pressed. Opening the website.")
        info_file = info_files[GROUP_ID]
        debug_print("Selected file is:", info_file, "\n")
        info_txt = info_dir+info_file
        debug_print("Info file path is:", info_txt)
        debug_print("Opening info file for reading..")
        info_txt_open = open(info_txt, 'r')
        debug_print("Done.\n")
        url = info_txt_open.readline()

        webbrowser.open(url)


# FIX TEXT RESOLUTION
def fix_text_resolution():
    """Function to fix text resolution.
    Default resolution is 1.0 (72dpi).
    """
    scene = bge.logic.getCurrentScene()

    debug_print("Text resolution is:", scene.objects["info_text"].resolution)
    if scene.objects["info_text"].resolution != 32.0:
        scene.objects["info_text"].resolution = 32.0
        debug_print("Text changed resolution is:", scene.objects["info_text"].resolution)


# CAMERA_POSITION

def set_camera_position():
    """Set the camera's position."""
    controller = bge.logic.getCurrentController()
    own = controller.owner

    debug_print(own.worldOrientation)

    # Setup the sensors.
    Num1 = controller.sensors["Num1"]
    Num2 = controller.sensors["Num2"]
    Num3 = controller.sensors["Num3"]
    Num4 = controller.sensors["Num4"]
    Num5 = controller.sensors["Num5"]
    Num6 = controller.sensors["Num6"]
    Num7 = controller.sensors["Num7"]
    Num8 = controller.sensors["Num8"]
    Num9 = controller.sensors["Num9"]

    # Setup the conditions for the camera position and orientation
    # SW (southwest)
    if Num1.positive:
        debug_print("Seting the camera to the SOUTHWEST position.")
        own.worldPosition = [-32.0, -32.0, 44.0]
        own.worldOrientation = [
            [0.7071, 0.5000, -0.5000],
            [-0.7071, 0.5000, -0.5000],
            [-0.0000, 0.7071,  0.7071]
        ]
    # S (south)
    if Num2.positive:
        debug_print("Seting the camera to the SOUTH position.")
        own.worldPosition = [0.0, -44.0, 44.0]
        own.worldOrientation = [
            [1.0000, 0.0000,  0.0000],
            [0.0000, 0.7071, -0.7071],
            [-0.0000, 0.7071,  0.7071]
        ]
    # S (south)
    if Num3.positive:
        debug_print("Seting the camera to the SOUTHEAST position.")
        own.worldPosition = [32.0, -32.0, 44.0]
        own.worldOrientation = [
            [0.7071, -0.5000,  0.5000],
            [0.7071,  0.5000, -0.5000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # W (west)
    if Num4.positive:
        debug_print("Seting the camera to the WEST position.")
        own.worldPosition = [-44.0, -0.0, 44.0]
        own.worldOrientation = [
            [-0.0000,  0.7071, -0.7071],
            [-1.0000, -0.0000,  0.0000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # O (Original position)
    if Num5.positive:
        debug_print("Reseting the camera to its original position.")
        own.worldPosition = [32.0, -32.0, 44.0]
        own.worldOrientation = [
            [0.7071, -0.5000,  0.5000],
            [0.7071,  0.5000, -0.5000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # E (east)
    if Num6.positive:
        debug_print("Seting the camera to the EAST position.")
        own.worldPosition = [44.0, 0.0, 44.0]
        own.worldOrientation = [
            [0.0000, -0.7071,  0.7071],
            [1.0000,  0.0000, -0.0000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # NW (northwest)
    if Num7.positive:
        debug_print("Seting the camera to the NORTHWEST position.")
        own.worldPosition = [-32.0, 32.0, 44.0]
        own.worldOrientation = [
            [-0.7071,  0.5000, -0.5000],
            [-0.7071, -0.5000,  0.5000],
            [-0.0000,  0.7071,  0.7071]
        ]
    # N (north)
    if Num8.positive:
        debug_print("Seting the camera to the NORTH position.")
        own.worldPosition = [0.0, 44.0, 44.0]
        own.worldOrientation = [
            [-1.0000, -0.0000, 0.0000],
            [0.0000, -0.7071, 0.7071],
            [-0.0000,  0.7071, 0.7071]
        ]
    # NE (northeast)
    if Num9.positive:
        debug_print("Seting the camera to the NORTHEAST position.")
        own.worldPosition = [32.0, 32.0, 44.0]
        own.worldOrientation = [
            [-0.7071, -0.5000, 0.5000],
            [0.7071, -0.5000, 0.5000],
            [-0.0000,  0.7071, 0.7071]
        ]


# SCREENSHOT
def take_screenshot():
    """Function to take a screenshot.
    Requires Imagemagick in Linux.
    Windows support is in the TODO list.
    """
    controller = bge.logic.getCurrentController()
    debug_print("The controller is:", controller)
    own = controller.owner
    debug_print("The owner is:", own)

    scene = bge.logic.getCurrentScene()
    debug_print("Current scene is:", scene)

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
        debug_print("Taking screenshot...")
        subprocess.run(screenshot_args)


# PHASE 2: MAIN


def main():
    """The main function (MAIN scene) that controls everything."""
    controller = bge.logic.getCurrentController()
    own = controller.owner

    #The Sensors (attached to MAIN scene's camera).
    #Left click, Right Click and Mouse Over
    left_click = controller.sensors["left_click"]
    right_click = controller.sensors["right_click"]
    mouse_over = controller.sensors["mouse_over"]
    # Snapping mode sensors:
    # 1 for center of face.
    # 2 for 1/10th of face's potision.
    # 3 for free snap.
    mode_1 = controller.sensors["mode_1"]
    mode_2 = controller.sensors["mode_2"]
    mode_3 = controller.sensors["mode_3"]

    global MODE

    if mode_1.positive:
        debug_print("Mode 1 is active. Snapping to center of face.")
        MODE = 1
        debug_print("Mode is:", MODE)
    if mode_2.positive:
        debug_print("Mode 2 is active. Snapping to 1/10th of face's position.")
        MODE = 2
        debug_print("Mode is:", MODE)
    if mode_3.positive:
        debug_print("Mode 3 is active. Snapping freely on the face.")
        MODE = 3
        debug_print("Mode is:", MODE)


    preview.position = ghost.position  # The preview's position is the same as the ghost's position. Updates constantly.
    preview.worldOrientation = ghost.worldOrientation  # Same for the orientation (rotation)

    # MOUSE_OVER - The "mouse over" function
    if mouse_over.positive and mouse_is_over_button == 1:

        debug_print("The mouse is over a button.")

        # Get the object that the ray hit
        rayObj = mouse_over.hitObject
        debug_print("The object hit by the ray is:", rayObj)
        debug_print("Ray object's world position is:", rayObj.worldPosition)

        # Get the object's normal face
        rayNormal = mouse_over.hitNormal
        debug_print("The object normal is:", rayNormal)
        debug_print(" rayNormal[0] is:", rayNormal[0], "\n", "rayNormal[1] is:", rayNormal[1], "\n", "rayNormal[2] is:", rayNormal[2], "\n",)

        # Get the ray's position
        rayPos = mouse_over.hitPosition
        debug_print("The ray's position is: ", rayPos)
        debug_print("The ray's X position is: ", rayPos[0])
        debug_print("The ray's Y position is: ", rayPos[1])
        debug_print("The ray's Z position is: ", rayPos[2])
        debug_print("\n")

        debug_print(rayObj.worldOrientation)

        # PLACE - Place the ghost object on the side of the object the mouse is over of,
        # according to the object's dimensions.
        # X axis - positive
        if round(rayNormal[0], 2) == 1:
            if MODE == 1:
                ghost.worldPosition = [rayPos[0] + float(length)/2, rayObj.worldPosition.y, rayObj.worldPosition.z]
            if MODE == 2:
                ghost.worldPosition = [rayPos[0] + float(length)/2, round(rayPos[1], 1), round(rayPos[2], 1)]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0] + float(length)/2, rayPos[1], rayPos[2]]
        # X axis - negative
        if rayNormal[0] == -1:
            if MODE == 1:
                ghost.worldPosition = [rayPos[0] - float(length)/2, rayObj.worldPosition.y, rayObj.worldPosition.z]
            if MODE == 2:
                ghost.worldPosition = [rayPos[0] - float(length)/2, round(rayPos[1], 1), round(rayPos[2], 1)]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0] - float(length)/2, rayPos[1], rayPos[2]]

        # Y axis - positive
        if rayNormal[1] == 1:
            if MODE == 1:
                ghost.worldPosition = [rayObj.worldPosition.x, rayPos[1] + float(width)/2, rayObj.worldPosition.z]
            if MODE == 2:
                ghost.worldPosition = [round(rayPos[0], 1), rayPos[1] + float(width)/2, round(rayPos[2], 1)]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0], rayPos[1] + float(width)/2, rayPos[2]]
        # Y axis - negative
        if rayNormal[1] == -1:
            if MODE == 1:
                ghost.worldPosition = [rayObj.worldPosition.x, rayPos[1] - float(width)/2, rayObj.worldPosition.z]
            if MODE == 2:
                ghost.worldPosition = [round(rayPos[0], 1), rayPos[1] - float(width)/2, round(rayPos[2], 1)]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0], rayPos[1] - float(width)/2, rayPos[2]]

        # Z axis - positive
        if rayNormal[2] == 1:
            if MODE == 1:
                ghost.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayPos[2] + float(height)/2]
            if MODE == 2:
                ghost.worldPosition = [round(rayPos[0], 1), round(rayPos[1], 1), rayPos[2] + float(height)/2]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0], rayPos[1], rayPos[2] + float(height)/2]
        # Z axis - negative
        if rayNormal[2] == -1:
            if MODE == 1:
                ghost.worldPosition = [rayObj.worldPosition.x, rayObj.worldPosition.y, rayPos[2] - float(height)/2]
            if MODE == 2:
                ghost.worldPosition = [round(rayPos[0], 1), round(rayPos[1], 1), rayPos[2] - float(height)/2]
            if MODE == 3:
                ghost.worldPosition = [rayPos[0], rayPos[1], rayPos[2] - float(height)/2]

        # ADD/DELETE
        # ADD - Add object when you left click
        if left_click.positive and mouse_is_over_button == 1:

            debug_print("Left mouse button has been clicked.")

            # Adds an object (item) at the position of the ghost (ghost) at the frame 0 ### Maybe I can use the frames to do the UNDO function. TODO
            obj = scene.addObject(item, ghost, 0)
            bbox = scene.addObject("bounding_box", ghost, 0)

            #bbox.worldScale = (float(length), float(width), float(height))

            # LOCATION
            # Location of the newly added objects (same as the ghost's position).
            obj.worldPosition = ghost.worldPosition
            bbox.worldPosition = ghost.worldPosition
            # ROTATION
            # Orientation of the new objects (same as the ghost's rotation).
            obj.worldOrientation = ghost.worldOrientation
            bbox.worldOrientation = ghost.worldOrientation

        # DELETE
        # Delete object
        if right_click.positive:
            rayObj.endObject()
