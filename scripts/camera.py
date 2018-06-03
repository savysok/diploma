import bge

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
