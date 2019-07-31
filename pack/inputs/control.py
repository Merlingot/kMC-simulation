#File containing the infos to run the kmc simulation
#TODO : saving frequency

# number of steps
nsteps = 100
# size of simulation
nx = 20
ny = 20
# temperature of substrate
temperature=300
# deposition rate
deposition_rate=50

# absolute path to the package directory (<mypath>/pack/)
packdir = "/Users/mariannelado-roy/kmc-simulation/pack/"

# path to the file where the results of the simulation will be written
resultFile = packdir + "out/results.txt"

# path to the directory where the position of the atoms will be written
coordDir = packdir + "out/coordinates/"

# path to the directory where to save the frames
frameDir = packdir + "out/frames/"

# path to the file where the domain lenght will be written
rangeFile = packdir + "out/range.txt"

# path and name of the file where the unregistered configurations will be written.
undefinedFile = packdir + "out/undefined.txt"

# path to the gif file
gifFile = packdir + "out/mygif.gif"
