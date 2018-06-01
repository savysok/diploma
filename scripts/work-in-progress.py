### Function to take the dimensional properties of an item (WIP)(NOT WORKING)

def create_item_properties_list():

    global merged_item_property_list
    merged_item_property_list = []

    files = [f for f in os.listdir(data_directory)]
    for f in files:
        csv_file = data_directory+f
        #print(csv_file)
        with open(csv_file) as N:
            #print(csv_file,"is open")
            reader = csv.reader(N, delimiter=',')
            for row in reader:
                if not "NAME" in row:
                    #print(row)
                    merged_item_property_list.append(row)

    print(merged_item_property_list)
    print("\n")

# create_item_properties_list()


### ROTATION (NOT WORKING) - When the object is rotated 90 degrees, the length and width parameters get switched. Needs more work cause it doesn't work very good.
def object_dimensions(rotation):

    global width
    global length

    if rotation == 0:
        #print("Rotation is 0 degrees")
        width = float(i_width[new_ID])
        #print("Width is",width)
        length = float(i_length[new_ID])
        #print("Length is",length,"\n")
    if rotation == 1:
        #print("Rotation is 90 degrees")
        width = float(i_length[new_ID])
        #print("Width is",width)
        length = float(i_width[new_ID])
        #print("Length is",length,"\n")

# object_dimensions(0)

def preview_mesh_orentation():      ### Function that tells the program that the object is rotated so that it switches the width and length parameters. Needs more work.

    controller = bge.logic.getCurrentController()
    #print("The controller is:",controller)
    own = controller.owner
    #print("Owner is:",own)

    print(own.worldOrientation)

    R_button = controller.sensors["R"]
    shift = controller.sensors["shift"]
    mouse_wheel_up = controller.sensors["mouse_wheel_up"]
    mouse_wheel_down = controller.sensors["mouse_wheel_down"]

    orientation = round(own.worldOrientation[0][0],2)

    if orientation >= 0.8 or orientation <= -0.8:
        if R_button.positive or shift.positive and mouse_wheel_up.positive or shift.positive and mouse_wheel_down.positive:
        #print(round(own.worldOrientation[0][0],2))
            orientation = round(own.worldOrientation[0][0],2)
            print("Orientation is:",orientation)
            object_dimensions(0)
    if orientation <= 0.1 and orientation >= -0.1:
        if R_button.positive or shift.positive and mouse_wheel_up.positive or shift.positive and mouse_wheel_down.positive:
            orientation = round(own.worldOrientation[0][0],2)
            print("Orientation is:",orientation)
            object_dimensions(1)


### BBox DIMENSIONS (WIP)

def bounding_box_dimensions(): ### Function that scales the bounding box with the

    controller = bge.logic.getCurrentController()
    own = controller.owner

    own.worldScale = (float(width), float(length), float(height))
    #print("Own world orientation:\n",own.worldOrientation)
    #print("Width is:",width)
    #print("Length is:",length)
    #print("Height is:",height)
