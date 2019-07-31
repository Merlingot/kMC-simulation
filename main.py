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
import inputs.control as ctrl
import inputs.processes as prc
# source code
import src.kmc as kmc
from src.initFunc import init
from src.run import doSteps
from src.saveFuncs import writeResults, writePositions


def main():

	# Assing process list to kmc module
	kmc.proc_list = pcr.list_of_processes

	# Initialization
	init(ctrl.area, ctrl.deposition_rate, ctrl.temperature)

	# Run n steps
	status=doSteps(ctrl.nsteps, ctrl.posFile, ctrl.undefinedFile, ctrl.total_deposition_rate)

	# Saving
	writeResults(ctrl.resultFile, status)
	writePositions(ctrl.posFile)

	return status


#### EXECUTE SIMULATION ####
status = main()
print(status)
############################
