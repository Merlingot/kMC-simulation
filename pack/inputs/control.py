# Sample of control file

# number of kmc steps
nsteps = 100
# number of repetition of the unit cell
# for reference the size of the unit cell is a/2 x 2*a/sqrt(3)
nx = 10
ny = 10
# temperature of substrate (Kelvin)
temperature=300
# deposition rate (Angstrom/second)
deposition_rate=50
# size of island triangle
# lisland = (4.28*1e-10/2)*20
lisland = 0

# relative path to the package directory (<packdir> = <kmcDir>/pack/)
packdir = "pack/"
# relative path to the output directory (<outdir>)
outdir =  "out/"

# relative path to the directory where the coordinates of occupied sites
coorddir = outdir + "coordinates/"
# relative to the directory where to save the frames
framesdir = outdir + "frames/"

# Memory usage file
memFile = outdir + "memory.txt"
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
