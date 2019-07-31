#------------------------------------------------------
# Executable file: main
# Description: file to be executed to run a simulation
# 			   not interactively.
# How to run:
# 	$ cd <simudir>
# 	$ python <dir>/main
# Function included :
#	- main
#------------------------------------------------------

import numpy as np

# input files
import pack.inputs.control as ctrl
import pack.inputs.processes as prc
# package
import pack.src.kmc as kmc
from pack.src.initFuncs import init
from pack.src.run import doSteps
from pack.src.saveFuncs import writeResults, writeRange


def main():

	# Assing process list to kmc module
	kmc.proc_list = prc.list_of_processes

	# Initialization
	print('Initialization ...')
	init(ctrl.nx, ctrl.ny, ctrl.deposition_rate, ctrl.temperature)

	# Run n steps
	print('Start of simulation')
	status=doSteps(ctrl.nsteps, ctrl.coordDir, ctrl.undefinedFile, ctrl.frameDir)

	# Saving
	print('Saving results...')
	writeResults(ctrl.resultFile, status)
	writeRange(ctrl.rangeFile)

	print('Done')

	return status


#### EXECUTE SIMULATION ####
status = main()
############################
