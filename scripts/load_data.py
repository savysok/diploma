import bge
import csv
from config import custom_dir
from csv import DictReader
from main import clear_grid, debug_print, scene, ghost


# CREATE_BUILDING
def create_building(CSVfile):
    """Function to create a building from CSV file.
    First, deletes all the previous objects.
    """
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    object_list = [obj for obj in scene.objects]
    excluded_objects = ['light', 'camera', 'preview', 'ghost', 'button', 'message', 'listener']
    for obj in object_list:
        name = obj.name
        if not any(excluded_objects in name for excluded_objects in excluded_objects):
            obj.endObject()
    
    DataFile = custom_dir+CSVfile  # The CSVfile that holds the instructions

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
    
    
# LOAD DATA
def load_data():
    """Function to load the data from the external file."""
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    left_click_button = controller.sensors["left_click_button"]
    mouse_over_button = controller.sensors["mouse_over_button"]
    
    load_slot = own["ID"]
    
    if left_click_button.positive and mouse_over_button.positive:
        load_file = "custom00"+str(load_slot)+".csv"
        create_building(load_file)
    