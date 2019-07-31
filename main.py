#------------------------------------------------------
# File: main
# Description: file to be executed to run a simulation
#              not interactively.
# 			   How to run: $ python <dir>/main
# Function included :
#	- main
# Note :Only module to import from input files.
#------------------------------------------------------

import numpy as np

# input files
import pkg.inputs.control as ctrl
import pkg.inputs.processes as prc
# source code
import pkg.src.kmc as kmc
from pkg.src.initFuncs import init
from pkg.src.run import doSteps
from pkg.src.saveFuncs import writeResults, writeRange


def main():

	# Assing process list to kmc module
	kmc.proc_list = prc.list_of_processes

	# Initialization
	print('Initialization ...')
	init(ctrl.nx, ctrl.ny, ctrl.deposition_rate, ctrl.temperature)

	# Run n steps
	print('Start of simulation')
	status=doSteps(ctrl.nsteps, ctrl.posDir, ctrl.undefinedFile, ctrl.frameDir)

	# Saving
	print('Saving results...')
	writeResults(ctrl.resultFile, status)
	writeRange(ctrl.rangeFile)

	print('Done')

	return status


#### EXECUTE SIMULATION ####
status = main()
############################
