"""
Module: model.py
Description: Definition of the Model Class.
	     The Model Class is used to run the simulation interactively
"""

import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# includes
from constants import *
from lattice import Lattice
from site import Site
from result import Result

# utilities 
import kmc
import in.parameters as parameters
from initFunc import init
from utilities.genLattice import createLattice
from scr.runProc import put
from scr.runStep import doSteps




class Model():

    def __init__(self, list_of_processes, temperature, size, deposition_rate , name = None):
        """
        Args:
            name (str) : name to give to the model
            list_of_processes (List(Process)) : COMPLETE list of the processes
            temperature : temperature of substrate (K)
            deposition_rate : deposition rate (Angstrom/s)
            size : width of the area to be simulated (in micrometers^2)
        """
        self.name = name

        self.TEMPERATURE = temperature
        self.DEPOSITION_RATE = deposition_rate
        self.AREA = size**2
        self.REPETITIONS = parameters.calculateRepetitions(self.AREA)
        self.TOTAL_DEPOSITION_RATE = parameters.calculateTotalRate(self.AREA, self.DEPOSITION_RATE)

        # Mettre la liste de processus dans le kmc
        kmc.proc_list = list_of_processes
        self.calculateProcessRates() #Calculer les rates
        #Generer la lattice
        kmc.lattice = createLattice( self.REPETITIONS )
        #Assigner le taux de deposition
        #Initialisation
        init(self.TOTAL_DEPOSITION_RATE)


    def createIsland(self, frac):
        """
        creates an island in the domain
        Args:
            frac (int - [0,1[ ) : fraction of simulation domain occupied by island
        Returns:
            None
        """
        number = kmc.sites_count*frac
        if frac > 1 :
            print("Erreur | Model.py - createIsland() | l'argument fraction doit etre entre 0 and 1")
        else:
            i = 0
            reps = int(number/6)
            for rep in range(reps):
                for rep_ in range(4):
                    put(kmc.lattice.sites[i], 1)
                    i+= 1
                i+= 2

    def putAtoms(self, frac):
        """
        Puts n atoms on the surface at random places.
        Args:
            frac (int - [0,1[ ) : fraction of simulation domain occupied by island
        Returns:
            None
        """
        if frac > 1:
            print("Erreur | Model.py - putAtoms() | l'argument fraction doit etre entre 0 and 1")
        else:
            sample = random.sample(kmc.lattice.sites, k=n)
            for site in sample:
                put(site, 1)

    def run(self, n ):
        """
	Execute a number of steps
        Args:
            n (int) : number of steps to be executed
        Returns:
            stop (Bool) : if Bool, then no more processes can happen and simulation has to stop !
        """
        stop = doSteps( n )
        return stop

    def calculateProcessRates(self):
        """ Calculates process rates according to the parameters set in the parameters.py file """
        for proc in kmc.proc_list:
            proc.rate = proc.calculateRate( parameters.PREFACTOR, self.TEMPERATURE, parameters.BOLTZMAN )

    def printStats(self):
        """ Prints the processes' name and their occurence in % after simulation time """
        total = np.sum(kmc.process_stats)
        proc_stat = kmc.process_stats*100/total
        indexSort = np.argsort(proc_stat)
        for index in indexSort:
            if proc_stat[index] > 1: #Greater than 1%
                print( '{} | {:.2f}'.format( kmc.proc_list[index].name, proc_stat[index] ) )

    def printResults(self):
        """ Prints the results of the simulation """
        
	print('Nombre de sites: {} '.format(kmc.sites_count))
        print('Aire: {:.6f} microm^2'.format(self.AREA*1e12))
        print('Nombre de processus: {}'.format(kmc.nb_of_process))
        print('Temps initialisation (CPU): {:.6f} s.'.format(kmc.init_time) )
        average_time = np.mean(kmc.processor_time_steps)
        print('Temps moyen pour 1 pas kMC (CPU): {:.6f} s.'.format(average_time))
        print('Temps total (CPU) : {:.6f} s'.format(kmc.processor_time))
        print('Nombre de step: {}'.format(kmc.steps))
        print()
        print('Temps (systeme physique) : {:.6f} s'.format(kmc.time))
        print('Stats en pourcentage:')
        self.printStats()

    def writeResults(self, filename):
        """ Writes the results of the simulation """
        
	with open(filename, 'w+') as resultFile:
	
	resultFile.write('Nombre de sites: {} \n'.format(kmc.sites_count))
        resultFile.write('Aire: {:.6f} microm^2 \n'.format(self.AREA*1e12))
        resultFile.write('Nombre de processus: {}\n'.format(kmc.nb_of_process))
        resultFile.write('Temps initialisation (CPU): {:.6f} s.\n'.format(kmc.init_time) )
        average_time = np.mean(kmc.processor_time_steps)
        resultFile.write('Temps moyen pour 1 pas kMC (CPU): {:.6f} s.\n'.format(average_time))
        resultFile.write('Temps total (CPU) : {:.6f} s. \n'.format(kmc.processor_time))
        resultFile.write('Nombre de step: {} \n'.format(kmc.steps))
        
        resultFile.write('Temps (systeme physique) : {:.6f} s \n'.format(kmc.time))
        resultFile.write('Stats en pourcentage: \n')

	total = np.sum(kmc.process_stats)
        proc_stat = kmc.process_stats*100/total
        indexSort = np.argsort(proc_stat)
        for index in indexSort:
            if proc_stat[index] > 0: #Greater than 0
                resultFile.write( '{} | {} | {:.2f} \n'.format( kmc.proc_list[index].name, index, proc_stat[index] ) )

    def writePositions(self, filename):
	""" Writes the position of atoms and molecules to a file"     
	with open(filename, 'w+') as posFile:
            posFile.write('# Time: {} s. \n\n'.format(kmc.time))
	    for site in kmc.lattice.sites:
		if site.occupancy > 0:
		   posFile.write( sites.coordinates[0] + ' ' + sites.coordinates[1] + ' ' + site.occupancy + '\n' ) 
