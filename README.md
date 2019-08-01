# kMC-simulation
Kinetic Monte Carlo simulation of epitaxial growth of Antimonene

## Executing 
```
$ cd <kmcDir>
$ python main.py
```
## Input files
The kmc-simulation requires information from two input files, the control parameter file and the kmc processes data file. 
#### Control parameter file
File consisting of statements of the form:
``` 
parameter = value 
```
The parameters defined in this file are:
- Number of kmc steps
- Domain size
- Temperature
- Deposition rate
- Directories and file names for outputs
#### Processes data file
File in which the kmc processes must be defined. 
## Output files
#### Coordinates outputs
In the `<kmcDir>/out/coordinates/` directory  .txt files containing the coordinates of atoms and molecules are stored for each kmc step during the simulation. The header of the file specifies the step and the simulation time. 
#### Result files
The `<kmcDir>/out/results.txt` file contains the control parameters of the simulation and the kmc processes stats.
## Visualisation 
To make an animation from the results run: 
```
$ cd <kmcDir>
$ python do_animation.py
```





