#######################################################
# Executable file: main
# Description: file to be executed to run a simulation.
# How to run:
# 	$ cd <kmcDir>
# 	$ python main.py
# Function included :
#	- main
#######################################################
import numpy as np
import os

#memory and time profiling
from profile import profile
from time import sleep

# package functions
from pack.src.initFuncs import init, initDirectoriesandFiles, initIsland
from pack.src.run import doSteps
from pack.src.saveFuncs import writeResults, writeRange, writeStats, saveFrames, writeMemUsage

@profile
def main():

	# input files
	import pack.src.kmc as kmc
	import pack.inputs.control as ctrl
	import pack.inputs.processes as prc

	# Assing process list to kmc module
	kmc.proc_list = prc.list_of_processes

	# Initialization
	print('Initialization ...')
	initDirectoriesandFiles(ctrl.outdir, ctrl.coorddir, ctrl.framesdir, ctrl.undefinedFile, ctrl.procFile)
	init(ctrl.nx, ctrl.ny, ctrl.deposition_rate, ctrl.temperature)

	if ctrl.lisland>0 :
		initIsland(ctrl.lisland, ctrl.undefinedFile)

	# Run n steps
	print('Start of simulation')
	status=doSteps(ctrl.nsteps, ctrl.coorddir, ctrl.procFile, ctrl.framesdir, ctrl.undefinedFile)
	print('End of simulation')

	# Saving
	print('Saving results...')
	writeResults(ctrl.resultFile, status)
	writeStats(ctrl.statFile)
	writeRange(ctrl.rangeFile)
	writeMemUsage(ctrl.memFile)

	print('Done')

	return status


# Execute main function
main()
