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

# absolute path to the package directory (pkg)
simudir = "/Users/mariannelado-roy/kmc-simulation/pkg/"

# path to the file where the results of the simulation will be written
resultFile = simudir + "out/results.txt"

# path to the directory where the position of the atoms will be written
posDir = simudir + "out/coordinates/"

# path to the directory where to save the frames
frameDir = simudir + "out/frames/"

# path to the file where the domain lenght will be written
rangeFile = simudir + "out/range.txt"

# path and name of the file where the unregistered configurations will be written.
undefinedFile = simudir + "out/undefined.txt"
