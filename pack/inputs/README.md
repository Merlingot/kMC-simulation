
# Control Parameters

See example of control file. 

### Simulation parameters
Parameter | Type | Description
--- | --- | ---
`nsteps`| int  | maximal number of kmc steps
`nx`| int  | number of repetition of the unit cell in x
`ny`| int  | number of repetition of the unit cell in y
`temperature`| float | substrate temperature (Kelvin)
`deposition_rate`| float | deposition rate (Angstrom/second)

### I/O parameters 
All paths can be defined relatively to the `<kmcDir>` directory

Parameter | String | Description| Additional note
--- | --- | --- | ---
`packdir`| string | Package directory <kmcDir>/pack/ |
`outdir`| string| string | Principal output directory| Directory containing all output files.
`coordir`| string |  Output directory for coordinates files | At each kmc step, a .txt file will be written in that folder containing the coordinates of all occupied site and their occupancy. 
`framesdir`| string| Output directory for frames files | If enabled in the source code, at each kmc step, a png image of the lattice will be printed to this directory. This should only be used for verification purposes as it slows down the simulation considerably.
`resultFile `| string| Name and extension (.txt) of the result file|File where the informations and results of the simulation will be written. 
`rangeFile` | string| Name and extension (.txt) of the domain range file |File  where the domain lenght will be written.
`undefinedFile` | string| Name and extension (.txt) of undefined processes file |File where the unregistered configurations will be written.
`gifFile` | string| Name and extension (.gif) of the gif file| 
