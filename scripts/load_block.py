import bge
import csv
import math
from config import custom_dir
from csv import DictReader


# DEBUGGING
DEBUG=False
print("(Debugging is set to", DEBUG, ")\n")
def debug_print(*args):
    """Function that set the debugging mode On (True) or Off (False)"""
    if DEBUG:
        print(*args)
        

scene = bge.logic.getCurrentScene()
emitter = scene.objects["preview.block_emitter"]
preview = scene.objects["preview.block_preview"] # The building editor preview

#object_list = []


def create_object_list(CSVFile):
    """Function to create the list containing all the object data like
    part's name and location.
    """
    
    print("Creating the objects list")
    
    global object_list 
    object_list = []
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    DataFile = custom_dir+CSVFile  # The CSVfile that holds the instructions

    with open(DataFile, "r") as D:
        CSVreader = csv.reader(D, delimiter = ",")
        data = list(CSVreader)
        row_count = (len(data)-1) # Count the rows
        print("There are ", row_count, "rows of data")

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
    
    i = 0  # Start from the first row
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
        object_data = []
        object_data.append(items[i])
        object_data.append(x)
        object_data.append(y)
        object_data.append(z)
        object_data.append(r)
        i = i+1
        object_list.append(object_data)
    print("Object list:",object_list)
      
create_object_list("livingroom20180729151629.csv")
      
      
preview_block = []

def create_initial_block():
    """Function to create the initial block that will then move along
    with the building editor preview
    """
    
    i = 0
    while i < len(object_list):
        #print(object_list[i][0])
        global preview_block
        obj = scene.addObject(object_list[i][0], emitter, 0)
        obj.worldPosition = [object_list[i][1]+100 , object_list[i][2]-20, object_list[i][3]]
        xyz = obj.localOrientation.to_euler()
        xyz[2] = object_list[i][4]
        obj.localOrientation = xyz.to_matrix()
        preview_block.append(obj)
        i = i+1
    
    #print(preview_block)
    print("Finished creating the initial block.")


def move_block_to_preview():
    """Function to move the previewed block to the position
    of the block preview
    """
    
    i = 0
    while i < len(preview_block):
        preview_block[i].worldPosition.x = object_list[i][1] + preview.worldPosition.x
        preview_block[i].worldPosition.y = object_list[i][2] + preview.worldPosition.y
        preview_block[i].worldPosition.z = object_list[i][3] + preview.worldPosition.z
        
        xyz = preview_block[i].worldOrientation.to_euler()
        print(xyz)
        xyz[2] = object_list[i][4]
        preview_block[i].localOrientation = xyz.to_matrix()
        
        i = i+1
        

def place_block():
    
    #print(preview_block)
    i=0
    while i < len(preview_block):
        emitter.worldPosition = preview_block[i].worldPosition
        emitter.worldOrientation = preview_block[i].worldOrientation
        obj = scene.addObject(object_list[i][0], emitter, 0)
        #print("Placing block...")
        i = i+1
            
        
def rotate_block():
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    rot = controller.sensors["R"]
    
    if rot.positive:
        
        xyz = own.localOrientation.to_euler()
        xyz[2] = xyz[2] + math.pi/2
        new_orientation = round(xyz[2],3)
        own.localOrientation = xyz.to_matrix()
        
        angle = math.radians(90)
        
        i=0
        while i < len(preview_block):
            
            rotational_center = (0, 0)
            object_center = (object_list[i][1], object_list[i][2])
            
            initial_point = (object_center[0]-rotational_center[0], object_center[1]-rotational_center[1])
            new_point = (initial_point[0]*math.cos(angle)-initial_point[1]*math.sin(angle), initial_point[0]*math.sin(angle) + initial_point[1]*math.cos(angle))
            final_point = (new_point[0]+rotational_center[0], new_point[1]+rotational_center[1])

            object_list[i][1] = round(final_point[0],1)
            object_list[i][2] = round(final_point[1],1)
            
            object_list[i][4] = int(object_list[i][4]-new_orientation)
            
            i = i+1
        
        
        move_block_to_preview()