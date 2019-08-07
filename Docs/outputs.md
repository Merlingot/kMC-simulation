# Output directories and files 

#### Coordinates of occupied sites 
`<kmcDir>/out/<coorddir>/` 

In this directory will be saved the coordinates files. At each kmc step, a coordinate file is created is this directory. It contains 3 colums : the x y coordinates of the occupied sites and their occupation (0: empty, 1: atom, 4: Sb4).
#### Simulation size 
`<kmcDir>/out/<rangeFile>` 

This file contains the dimension in the x and y direction of the simulation cell.
#### Memory usage
`<kmcDir>/out/<memFile>` 

This file contains information about the memory usage of the simulation. First, the memory size of the process list and of the lattice objects. Second, the total memory usage of the program.
#### KMC processes statistics 
`<kmcDir>/out/<statsFile>`

This file contains the kmc processes statistic : the name of the processes, their type, their number and their occurence in %. 

`<kmcDir>/out/<procFile>`

At each step kmc, the kmc process that was selected is added to this file. The name of the process, its type, its number and its occurence for far are written. 
#### Results and informations 
`<kmcDir>/out/<resultFile>`

This files contains general about the simulation parameters and simuation time. 
#### Undefined processes
`<kmcDir>/out/<undefinesFile>`

This file contains the configuration number of all the unidentified processes encountered during a simulation. When a site posses a configuration which does not corresponds to any of the already defined processes, its configuration is written to this file. 
#### Visualisation
##### Frames
`<kmcDir>/out/frames/`

This directory contains the frames files. Theses files are .png images of the simulation cell at a given step. By default, a frame is saved before the first kmc and at the last one.

##### Animations 
`<kmcDir>/out/<gifFile>`

If the executable do_animation.py is executed, a gif file is created in the `<out>/`directory. 
