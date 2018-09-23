import bge

scene = bge.logic.getCurrentScene()

global level
level = 0

preview_space = scene.objects["preview.parts_space"]

def clear_block_grid():
    included_grids = ('grid_block', 
        'grid_block.bathroom', 'grid_block.bedroom', 
        'grid_block.kitchen', 'grid_block.livingroom'
        )
    for grid_object in scene.objects:
        #if grid_object.name == "grid_block":
        if any(included_grids in grid_object.name for included_grids in included_grids):     
            grid_object.endObject()
            
def clear_building_grid():
    for grid_object in scene.objects:
        if grid_object.name == "grid_building":
            grid_object.endObject()

def create_grid_pattern(size_x, size_y, x_origin, grid_block):
    n = -size_x  # This will start the grid symmetrically to the Y Axis to the negative value.
    while n < size_x:
        m = -size_y  # This will start the grid symmetrically to the X Axis to the negative value.
        while m < size_y:
            x = n  # This will place the grid object at the local position (pattern's X position) plus the distance it will repeat at, times n. ### TODO more explanation
            y = m  # This will place the grid object at the local position (pattern's Y position) plus the distance it will repeat at, times m. ### TODO more explanation
            z = level  # This will place the grid object at the local position (pattern's Z position). Currently the system I created doesn't allow me to create grid patterns in the 3d space. Only 2d.
            preview_space.worldPosition = [x+x_origin, y, z]  # This moves the ghost item to the new position, where it will replicate the grid object
            #print(preview.worldPosition)
            obj = scene.addObject(grid_block, preview_space, 0)  # This adds a grid object at the ghost's position
            m += 1
        n += 1

def generate_grid(level):
    """Function to create the grid.
    First clears the previous grids, then creates the new grid.
    """
       
    #clear_block_grid()
    #clear_building_grid()
    
    create_grid_pattern(6, 6, 0, "grid_block")
    create_grid_pattern(20, 20, 100, "grid_building")

def grid_level(height, max):
    
    controller = bge.logic.getCurrentController()
    own = controller.owner
    
    grid_up = controller.sensors["arrow_up"]
    grid_down = controller.sensors["arrow_down"]
    
    if grid_up.positive and own.worldPosition.z <= max:
        own.worldPosition.z += height
        
    if grid_down.positive and own.worldPosition.z > 0:
        own.worldPosition.z -= height

def block_grid():
    grid_level(3, 6)
    
def building_grid():
    grid_level(1, 12)
    