#File containing the infos to run the kmc simulation
#TODO : saving frequency

# number of steps
nsteps = 1000
# area of simulation
size=1e-8; area=size**2
# temperature of substrate
temperature=300
# deposition rate
deposition_rate=50

# absolute path to the simulation directory
simudir = "/mariannelado-roy/Documents/stage2018/"

# name of the file where the processes are defined
processfile = simudir + "in/processes.py"

# name of the file where the results of the simulation will be written
resultfile = simudir + "out/results.txt"

# name of the file where the position of the atoms will be written
posFile = simudir + "out/coordinates.txt"

# path and name of the file where the unregistered configurations will be written.
undefinedFile = simudir + "out/undefined.txt"
