#######################################################
# Executable file: main
# Description: file to be executed to run a simulation.
# How to run:
# 	$ cd <simudir>
# 	$ python main.py
# Function included :
#	- main
#######################################################

import numpy as np
import os

# package functions
from pack.src.initFuncs import init, initDirectoriesandFiles
from pack.src.run import doSteps
from pack.src.saveFuncs import writeResults, writeRange

def main():

	# input files
	import pack.src.kmc as kmc
	import pack.inputs.control as ctrl
	import pack.inputs.processes as prc

	# Assing process list to kmc module
	kmc.proc_list = prc.list_of_processes

	# Initialization
	print('Initialization ...')
	initDirectoriesandFiles(ctrl.outdir, ctrl.coorddir, ctrl.framesdir, ctrl.undefinedFile)
	init(ctrl.nx, ctrl.ny, ctrl.deposition_rate, ctrl.temperature)

	# Run n steps
	print('Start of simulation')
	status=doSteps(ctrl.nsteps, ctrl.coorddir, ctrl.undefinedFile, ctrl.framesdir)
	print('End of simulation')

	# Saving
	print('Saving results...')
	writeResults(ctrl.resultFile, status)
	writeRange(ctrl.rangeFile)

	print('Done')

	return status


# Execute main function
main()
