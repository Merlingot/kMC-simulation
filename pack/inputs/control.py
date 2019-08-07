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


# relative path to the package directory (<packdir> = <kmcDir>/pack/)
packdir = "pack/"
# relative path to the output directory (<outdir>)
outdir =  "out/"

# relative path to the directory where the coordinates of occupied sites
coorddir = outdir + "coordinates/"
# relative to the directory where to save the frames
framesdir = outdir + "frames/"


# relative path to the file where the kmc processes statistics will be written
statFile = outdir + "statistics.txt"
# relative path to the file where the kmc process selected at a step n will be written
procFile= outdir + "proc.txt"
# relative path to the file where the results of the simulation will be written
resultFile = outdir + "results.txt"
# relative path to the file where the domain lenght will be written
rangeFile = outdir + "range.txt"
# relative path and name of the file where the unregistered configurations will be written.
undefinedFile = outdir + "undefined.txt"
# relative path and name of the gif file
gifFile = outdir + "mygif.gif"
