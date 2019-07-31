#------------------------------------------------------
# Module: initFuncs
# Description: contains all functions for initilializing
#              the simulation
# Functions included:
#	- init
#	- initDepositionProcess
#	- initStatic
#	- initDynamic
#------------------------------------------------------

import time
import numpy as np

import pkg.src.kmc as kmc

from pkg.utilities.const import PREFACTOR, BOLTZMAN
from pkg.utilities.parameters import calculateDepositionArea, calculateTotalRate
from pkg.includes.latticeFunc import createLattice
from pkg.includes.procFuncs import createProcess


def init(nx, ny, deposition_rate, temperature):
    """
    Initializes all sites, lattice, book-keeping arrays.
    """
    t0 = time.clock()
    initLattice(nx, ny)
    initProcessRates(temperature)
    initDepositionProcess(nx,ny, deposition_rate)
    initStatic()
    initDynamic(kmc.total_deposition_rate)
    t1 = time.clock()
    kmc.init_time = t1 - t0

def initLattice(nx,ny):
    """Creates the lattice"""
    kmc.lattice = createLattice( np.array([nx,ny,0]) )

def initProcessRates(temperature):
    """Calculates the process rates given the temperature"""
    for proc in kmc.proc_list:
        proc.rate = proc.calculateRate(PREFACTOR, temperature, BOLTZMAN)

def initDepositionProcess(nx, ny, deposition_rate):
    """
    Create the deposition processes. Add them to the kmc.proc_list list.
    Because it is appended to kmc.proc_list, theses process are always the last ones.
    This has to be created appart because of the fact that the group rate (rate constant*nb of sites) has to be constant.

    Important: this is where is defined the main deposition process
    This deposition process implies the deposition of a Sb4 on the central site, with no other first neighbour.
    """
    kmc.area, kmc.lx, kmc.ly = calculateDepositionArea(nx,ny)
    kmc.total_deposition_rate = calculateTotalRate(kmc.area, deposition_rate)
    start_index = len(kmc.proc_list)
    dep =  createProcess( 'Deposition', 'deposition', shell = 1, empty = 0 )
    for proc in dep :
        proc.rate = kmc.total_deposition_rate #TO DO: assign directly
    kmc.proc_list +=  dep
    kmc.deposition_ids = np.arange(start_index, start_index+len(dep))


def initStatic():
    """ Initialise all static scalars and arrays belonging to the kmc module """

    kmc.time = 0; kmc.steps= 0; kmc.runtime = 0;
    kmc.proc_adress = {}
    count = 0
    for proc in kmc.proc_list:
        proc.number = count
        kmc.proc_adress.setdefault( proc.id , [] ).append( proc.number )
        count += 1
    kmc.nb_of_process  = len( kmc.proc_list )
    kmc.rate_constants = np.array( [ process.rate for process in kmc.proc_list ] )


def initDynamic(total_deposition_rate):
    """ Initialise all dynamic scalars arrays belonging to the kmc module"""

    kmc.runtime_steps = []
    kmc.sites_count = len(kmc.lattice.sites) #number of sites on the lattice
    kmc.process_stats = np.zeros( kmc.nb_of_process )
    kmc.nb_of_sites   = np.zeros( kmc.nb_of_process, dtype = int )
    kmc.active_sites  = [ [] for i in range(kmc.nb_of_process) ]
    kmc.adress_list = np.zeros( ( kmc.nb_of_process, kmc.sites_count ), dtype = int )
    kmc.lattice.initIds()
    initEvents()
    kmc.cumulative_rates = kmc.updateCumulRate()


def initEvents():
    """
    For each site in the lattice:
        - Find the processes that corresponds to its configuration id ( through the proc_adress )
        - Add an event (site, process) for each processes that can happen on this site
    """

    for site in kmc.lattice.sites :
        possible_processes_nb = kmc.proc_adress.get( site.id )
        if possible_processes_nb :
            for proc_nb in possible_processes_nb :
                kmc.addEvent( proc_nb, site.number )
