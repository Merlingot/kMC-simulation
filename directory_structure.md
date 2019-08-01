# Directory structure

## Main directory
`<kmcDir>/`    Contains the primary executable files main.py and do_animation.py
### Output sub directory
`<kmcDir>/out/` This directory will be created during the initialization of the simulation. All output files will be placed in this directory. 
### Package sub directory
Package required to run the executable files. Contains 5 sub packages.
##### Inputs
`<kmcDir>/pack/inputs` Directory containing the two input files: the control parameter file and the process data file. 
##### Source code
`<kmcDir>/pack/src` Python source code modules related to the executable files.
##### Include
`<kmcDir>/pack/includes` Python scripts consisting of definition of classes.  Python source code modules containing functions used to generate instances of the defined classes.
##### Utilities
`<kmcDir>/pack/utilities` Various support scripts. 
##### Tools
`<kmcDir>/pack/tools` Scripts and modules for the generation of animation. 
