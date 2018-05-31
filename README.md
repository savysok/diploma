# diploma
20180529

## Thesis project for N.T.U.A. 
###### by Spyros K.

This project is my thesis project for the N.T.U.A. 

The main idea is the creation of an architectural design program targeted at people not familiar with CAD (Computer Assisted Design/Drawing) type programs and allow them to create buildings using parts of famous buildings. The logic behind the building system is that of Lego/Froebel blocks/Minecraft: creating through the use of pre-determined building parts.

The project is currently under contstruction.

### Features:

- **modular building system**: create buildings from pre-modeled pieces 

- **"_point and click_"**: placement of the modular pieces with the click of a button

- **dynamic loading of models**: import your models blend file in the "models" subfolder and it will appear in the program next time you start it

### Folder structure:

- **custom**: a folder where all the custom models will be saved to be loaded

- **data**: the data folder has the csv with the item's name and dimensions. it has the format:
```
NAME,WIDTH,LENGTH,HEIGHT
cube.001,1.0,1.0,1.0
```

- **export**: the folder where the models will be exported. it consists of two subfolders, one "obj" and one "stl" folder. _(TODO: add more export formats)_

- **info**: the info folder. this is where the text that appears in the "Info" section of the program appears. also has the wikipedia link for the specific items _(TODO: add social media links also)_

- **models**: the main subfolder. it contains more subfolders, each with a different category of models. this folder is dynamically loaded in the program at startup and creates the lists and buttons accordingly _(TODO: more analysis here)_

- **screenshots**: this is where the screenshots from inside the program are saved. currently, it only works on linux with imagemagick installed. _(TODO: add Windows support if possible)_

- **scripts**: the scripts folder. this is where all the scripts are stored. I have tried to create as few script files as possible and put everything in the "main.py" script, although I don't know if that is a good pythonic practice. _(TODO: remove the unused/test scripts from the folder)_

- **textures**: this is the folder where I store all the project textures. all the Blender textures will be baked when the program is exported to standalone, so this folder is not needed. I keep it as a place where people can take my textures if they find them useful.

### Python modules:

csv & DictReader / os / textwrap / time / subprocess / webbrowser / math / mathutils / socket / select / sys / threading & Thread

Blender-specific: bge & logic / bpy & context 


### TODO

- **camera**(_optional_): 
  - [ ] camera movement (_improved_)
  - [ ] axonometric camera

- **grid**:
  - [ ] additional grid systems (_2d, 3d, famous grid systems_)
  - [ ] dynamic creation, saving and loading of grids
  - [ ] three-dimensional grids

- **interior design**:
  - [ ] walls (_window/windowless_)
  - [ ] grids
  - [ ] furniture (_chairs, tables, beds etc_)

- **3d models**:
  - [ ] bauhaus
  - [ ] eames house
  - [ ] athenian "_polykatoikia_"
