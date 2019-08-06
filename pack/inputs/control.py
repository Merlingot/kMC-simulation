# Sample of control file

# number of kmc steps
nsteps = 100
# number of repetition of the unit cell
nx = 20
ny = 20
# temperature of substrate (Kelvin)
temperature=300
# deposition rate (Angstrom/second)
deposition_rate=50

# absolute path to the simulation directory (<kmcDir>)
kmcDir = ""
# absolute path to the package directory (<packdir> = <kmcDir>/pack/)
packdir = kmcDir + "pack/"
# absolute path to the output directory (<outdir>)
outdir = kmcDir + "out/"

# path to the directory where the position of the atoms will be written
coorddir = outdir + "coordinates/"
# path to the directory where to save the frames
framesdir = outdir + "frames/"

# path to the file where the results of the simulation will be written
resultFile = outdir + "results.txt"
# path to the file where the domain lenght will be written
rangeFile = outdir + "range.txt"
# path and name of the file where the unregistered configurations will be written.
undefinedFile = outdir + "undefined.txt"
# path and name of the gif file
gifFile = outdir + "mygif.gif"
