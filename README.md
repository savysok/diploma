# diploma
20181005

## Thesis project for N.T.U.A.
###### by Spyros Kosyvas

This is my thesis project for the N.T.U.A. It is an experimentantion on creating a standalone architectural design program using exclusively open-source programs. It is inspired -among other things- by modular design and computer games.

The main idea was the creation of an architectural design program targeted at people not familiar with CAD (Computer Assisted Design/Drawing) type programs and allow them to create buildings using parts of buildings, such as walls, floors and furniture/appliances. The logic behind the building system is that of Lego/Froebel blocks: creating through the use of pre-defined building parts.

The project is currently a work-in-progress and under contstruction.


### Features:

- **modular building system**: create buildings from pre-modeled building pieces (Walls, Floors, Furniture/Appliances)

- **_point and click_**: placement of the modular pieces with the click of a button

- **save the creation**: save and load your creation


### TODO:

- **3d printing**: export your creation to .STL format, suitable for 3d printing (WIP)




### Examples:

**Block Editor**:
![Block Editor screenshot](https://imgur.com/XGWlti0.gif "Block Editor")
*single viewport (isometric view)*
Select your building blocks from left and add them in the grid space to the right.


**Block Editor**:
![Block Editor screenshot](https://imgur.com/4WVatBx.gif "Block Editor")
*split viewport (top and isometric views)*
Like the single viewport, add your pieces either on the top-down view or the isometric one. The blocks appear in both at the same time.


**Building Editor - split view**:
![Building Editor screenshot](https://imgur.com/VnN6Gjr.gif "Building Editor")
*split viewport (top and isometric block editor view on the left,
isometric building editor view on the right)*
Here you can create first some spaces on the right and work on them in detail on the left. More info for the feature coming soon.




### CONTROLS:

The program uses a few Keyboard keys and the Mouse.

![Keyboard Layout](https://imgur.com/P2h5Mdh.png "Keyboard Layout")

#### MOUSE:
- **Left click**: Select/Add Item
- **Right click**: Remove Item

#### KEYBOARD:
- **R button**: Rotate the Selected Item
- **SHIFT+R**: Rotate Item that the mouse pointer is pointing
- **SHIFT button** (hold): Hide the Selected Item

#### ARROW KEYS:
- **Left arrow key**: Rotate All Cameras Counter-clockwise 90 degrees
- **Right arrow key**: Rotate All Cameras Clockwise 90 degrees

- **Up arrow key**: Go up one level (move grid upwards)
- **Down arrow key**: Go down one level (move grid downwards)

#### BUILDING EDITOR CAMERA (only):
- **W button**: Move Camera up
- **A button**: Move Camera left
- **S button**: Move Camera down
- **D button**: Move Camera right
- **Mouse Wheel Up/Down**: Zoom in/out

- **Backspace**: Exit the program




### UI Buttons

The UI Buttons are located at the bottom of the screen and execute certain functions.


### System Buttons
These buttons execute system functions like Exit, Reload, Save and Load.
![System Buttons](https://imgur.com/GSw1QQt.jpg "System Buttons")

- **EXIT**: Exits the program
- **RELOAD**: Reloads the program from the start
- **SAVE**: Saves your current creation in a CSV file
- **LOAD**: Loads your previous creations, starting from the latest one first

### Camera Buttons
These buttons change the viewport layout of the screen, offering three ways to design.
![Camera Buttons](https://imgur.com/5OboE5s.jpg "Camera Buttons")

- **Viewport 1**: Single isometric view. This is the initial screen
- **Viewport 2**: Split view: Top and Isometric views. Items you place in one appear at the other.
- **Viewport 3**: Split view with the Space Organizer: Left are the Top and Isometric views, right is the Space Organizer view. More info on the Space Organizer coming soon.


### Set Buttons
These buttons change the sets of pieces available to create a building.
![Set Buttons](https://imgur.com/hTKhyVt.jpg "Set Buttons")
- **Light gray button**: Architectural pieces sets. Cycle through all the availabe architectural pieces, like Walls, Floors, Windows etc.
- **Dark gray button**: Furniture and Appliances pieces sets. Cycle through the available furniture and/or house appliances pieces, like kitchens, beds, chairs etc.

More info about the program and its functions are coming soon..




### PROGRAMS
All the programs used in the creation of the program are free and open-source.

- **[Blender](https://www.blender.org/ "Blender")**
- **[Python](https://www.python.org/ "Python")**
- **[GIMP](https://www.gimp.org/ "GIMP")**
- **[Inkscape](https://inkscape.org/en/ "Inkscape")**

- The program was created in [Ubuntu](https://www.ubuntu.com/ "Ubuntu") 16.04/18.04
