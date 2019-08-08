
# Control Parameters

See example of control file. 

### Simulation parameters
Parameter | Type | Description
--- | --- | ---
`nsteps`| int  | maximal number of kmc steps
`nx`| int  | number of repetition of the unit cell in x
`ny`| int  | number of repetition of the unit cell in y
`lisland`| float | side size of triangular island (set to None for no island)
`temperature`| float | substrate temperature (Kelvin)
`deposition_rate`| float | deposition rate (Angstrom/second)

### I/O parameters 
All paths can be defined relatively to the `<kmcDir>` directory

Parameter | String | Description| Additional note
--- | --- | --- | ---
`packdir`| string | Package directory |
`outdir`| string| string | Principal output directory| Directory containing all output files.
`coordir`| string |  Output directory for coordinates files | At each kmc step, a .txt file will be written in that folder containing the coordinates of all occupied site and their occupancy. 
`framesdir`| string | Output directory for frames files | If enabled in the source code, at each kmc step, a png image of the lattice will be printed to this directory. This should only be used for verification purposes as it slows down the simulation considerably.
'memFile' | string | Name and extenstion (.txt) of the memory usage statistic file |
`statsFile `| string | Name and extension (.txt) of the kmc processes statistics file| At the end of the simulation, the statistic of the kmc processes (name, type, number and occurence in %) will be written.
`resultFile `| string | Name and extension (.txt) of the result file| At the end of the simulation, the informations and results of the simulation will be written. 
`rangeFile` | string | Name and extension (.txt) of the domain range file |File  where the domain lenght will be written.
`procFile` | string | Name and extension (.txt) of the processes file | At each kmc step, the selected process for this step will be written (name of the process, type, number, occurence so far).
`undefinedFile` | string | Name and extension (.txt) of undefined processes file |File where the unregistered configurations will be written during the simualtion.
`gifFile` | string | Name and extension (.gif) of the gif file| 
