"""
Module: main
Description: blabla

Functions included :
	- main
	- writeResults
	- writePositions
"""

import numpy as np
import kmc

from in.control import temperature, deposition_rate, size, nsteps, resultFile, posFile, undefinedFile
from inputs.processes import list_of_processes
from parameters import calculateRepetitions, calculateTotalRate, PREFACTOR, BOLTZMAN
from initFunc import init
from utilities.genLattice import createLattice
from scr.runProc import put
from scr.runStep import doSteps
from scr.saveFuncs import writeResults, writePositions


def main():	
	# area of simulation domain
	area = size**2
	total_dep_rate = calculateTotalRate(area, deposition_rate)
	# Mettre la liste de processus dans le module kmc
	kmc.proc_list = list_of_processes
	#Calculer les rates
	for proc in kmc.proc_list:
	proc.rate = proc.calculateRate( PREFACTOR, temperature, BOLTZMAN )
    	#Generer la lattice
    	kmc.lattice = createLattice( calculateRepetitions(area) )
    	#Lancer l'initialisation
    	init(total_dep_rate)

	status=doSteps(nsteps, posFile, undefinedFile, total_deposition_rate)
	
	# Saving
	writeResults(resultFile, status)
	writePositions(posFile)

	return status


#### EXECUTE SIMULATION ####
main()
############################
