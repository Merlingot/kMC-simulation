#######################################################
# Module: runProc
# Description: functions needed to run a kmc step & to
#              execute a specific process on a specific
#              lattice site.
# Functions included:
#   - doSteps
#   - decisionTree
#	- put
#	- remove
#	- diffusion
#	- createMolecule
#	- separateMolecule
#   - writeUndefined
#######################################################


import numpy
import math
import random
import time

import pack.src.kmc as kmc
from pack.src.saveFuncs import writePositions, saveFrames, writeQuickStats
from pack.include.process import Diffusion, Evaporation, Deposition, MolCreation, MolDissociation


def doSteps( n, coorddir, procFile, framesdir, undefinedFile):
    """
    Performs n kMC step.
    Args
        n (int) : Number of kMC steps to run
	undefinedFile (str) : file name to write undefined configurations
	coorddir (str) : directory where to write coordinates of atoms
	TOTAL_DEPOSITON_RATE (float) : total deposition rate
    Returns
        stop (Bool) : indicates if the simulation had to be stopped
	       	      before the n steps were completed due to some reason.
    """
    steps_done = 0
    stop = False

    # save the first frame
    saveFrames( framesdir, kmc.steps)

    while steps_done < n:
        t0 = time.clock()
        selected_process_nb, selected_site_nb = kmc.selectEvent()

        if selected_process_nb != 'stop':

            PROC = kmc.proc_list[ selected_process_nb ]
            SITE = kmc.lattice.getSite( selected_site_nb )

            # safety net ----------------------------------
            assert (PROC.conf == SITE.conf), 'unmatching event has been selected'
            #----------------------------------------------

            decisionTree(PROC, SITE, undefinedFile)

            kmc.time += kmc.updateTime()
            kmc.cumulative_rates = kmc.updateCumulRate()

            t1 = time.clock()
            kmc.runtime_steps.append(t1-t0)
            kmc.runtime += t1-t0

            steps_done += 1
            kmc.steps += 1
            print( 'step: {} | process: {} | time: {:.6f} | runtime: {:.6f}'.format( kmc.steps,  PROC.name, kmc.time, kmc.runtime  ) )

            writePositions('{}coord_{}.txt'.format(coorddir, steps_done))
            writeQuickStats(procFile, PROC)

            # saveFrames: This will save an image of each step of the simulation. Only for testing purpose. Will slow down the simulation and take enormous space. Uncomment next line to activate.
            # saveFrames( framesdir, kmc.steps)

        else:
            stop = True
            print('Simulation has been stopped after the completion of the kmc step # {}'.format(kmc.steps ) )
            break

    # save the last frame
    saveFrames( framesdir, kmc.steps)

    return stop


def decisionTree(PROC, SITE, filename):

    """
    Runs a process on a site. Update all Bookeeping arrays.
    Args:
        proc (Process): Process instance, the process that is going to be executed
        site (Site) : Site instance, where the process is happening (center atom in CWIP)
    Returns:
        None
    """

    if PROC.__class__ == Diffusion:
        """diffusion:
        Implies the movement of only 1 object (atom, Sb2 or Sb4) from the central site to another
        """
        diffusion( SITE, SITE.neighbours[ PROC.next_site - 1 ], filename )

    elif PROC.__class__ == Evaporation:
        """evaporation:
        Implies the evaporation of only 1 object (atom, Sb2 or Sb4) from the central site
        evaporation.action_sites = None
        """
        remove(SITE, filename)

    elif PROC.__class__  == Deposition:
        """
        Implies the creation and deposition of a Sb4 on the lattice.
        """
        put(SITE, 4, filename)

    elif PROC.__class__ == MolCreation:
        """
        Implies that we take 4 atoms already existing and merge them into 1 site to form an Sb4
        """
        if new_site_nb == 0:
            NEW = SITE
            OLDS = [SITE.neighbours[i-1] for i in PROC.atom_sites if i!=0]
        else :
            NEW = SITE.neighbours[ PROC.mol_site-1 ]
            OLDS = []
            for i in PROC.atom_sites:
                if i!=0:
                    OLDS.append(SITE.neighbours[i-1])
                elif i == 0:
                    OLDS.append(SITE)

        createMolecule(OLDS, NEW, filename)


    elif PROC.__class__ == MolDissociation :
        """
        implies that we take 4 atoms (Sb4) already existing atoms that are merged on 1 site (central cwid) and separate them on 4 different sites.
        """
        NEWS = []
        for i in PROC.atom_sites :
            if i == 0:
                NEWS.append(SITE)
            else :
                NEWS.append(SITE.neighbours[i-1])

        separateMolecule(SITE, NEWS, filename)



def put(SITE, nb_of_atoms, filename):
    """
    Put a new object (atom or multiple atoms) on a site, then updates the data in kmc.
    Args :
        SITE: Site instance
        nb_of_atoms: number of atoms to put on this site
	f (str) : filename where to write unrecognized processes
    """
    processes_to_delete = kmc.proc_adress.get( SITE.conf )

    if processes_to_delete:
        for proc in processes_to_delete:
            kmc.delEvent(proc, SITE.number)
    else:
        writeUndefined(SITE.conf, filename)


    for neighbour in SITE.neighbours:
        _processes_to_delete = kmc.proc_adress.get( neighbour.conf )
        if _processes_to_delete:
            for proc in _processes_to_delete :
                kmc.delEvent(proc, neighbour.number)
        else :
            writeUndefined(neighbour.conf, filename)


    SITE.occupancy += nb_of_atoms
    # safety net --------------------
    assert (SITE.occupancy < 5), 'More than 4 atoms on site'
    # -------------------------------

    SITE.updateConf()
    processes_to_add = kmc.proc_adress.get( SITE.conf )
    if processes_to_add:
        for proc in processes_to_add :
            kmc.addEvent(proc, SITE.number)
    else :
        writeUndefined(SITE.conf, filename)


    for neighbour in SITE.neighbours:
        neighbour.updateConf()
        _processes_to_add = kmc.proc_adress.get( neighbour.conf )
        if _processes_to_add:
            for proc in _processes_to_add :
                kmc.addEvent(proc, neighbour.number)
        else:
            writeUndefined(neighbour.conf, filename)




def remove(SITE, filename):
    """
    Remove an existing species (atom, molecule) completetly from the site and the lattice, then updates the datakmc.
    Args:
        SITE : Site class instance

    """

    processes_to_delete = kmc.proc_adress.get( SITE.conf )
    if processes_to_delete:
        for proc in processes_to_delete :
            kmc.delEvent(proc, SITE.number)
    else:
        writeUndefined(SITE.conf, filename)



    for neighbour in SITE.neighbours:
        _processes_to_delete = kmc.proc_adress.get( neighbour.conf )
        if _process_to_delete :
            for proc in _processes_to_delete :
                kmc.delEvent(proc, neighbour.number)
        else :
            writeUndefined(neighbour.conf, filename)

    SITE.occupancy = 0


    SITE.updateConf()
    processes_to_add = kmc.proc_adress.get( SITE.conf )
    if processes_to_add:
        for proc in processes_to_add :
            kmc.addEvent(proc, SITE.number)
    else:
        writeUndefined(SITE.conf, filename)


    for neighbour in SITE.neighbours:
        neighbour.updateConf()
        _processes_to_add = kmc.proc_adress.get( neighbour.conf )
        if _processes_to_add:
            for proc in _processes_to_add :
                kmc.addEvent(proc, neighbour.number)
        else :
            writeUndefined(neighbour.conf, filename)




def diffusion(OLD, NEW, filename):
    """
    Moves an object from the central site to another site, then updates the data in kmc.
    """

    nb_list = list( OLD.neighbours_nb |  NEW.neighbours_nb )
    site_list = list ( kmc.lattice.getSite( site ) for site in nb_list )

    for site in site_list:
        processes_to_delete = kmc.proc_adress.get( site.conf )
        if processes_to_delete:
            for proc in processes_to_delete :
                kmc.delEvent(proc, site.number)
        else:
            writeUndefined(site.conf, filename)


    NEW.occupancy = OLD.occupancy
    OLD.occupancy = 0

    # safety net --------------------
    assert (NEW.occupancy  < 5), 'More than 4 atoms on site'
    # -------------------------------

    for site in site_list:
        site.updateConf()
        processes_to_add = kmc.proc_adress.get( site.conf )
        if processes_to_add :
            for proc in processes_to_add :
                kmc.addEvent(proc, site.number)
        else :
            writeUndefined(site.conf, filename)




def createMolecule(OLDS, NEW, filename):

    """ Takes existing atoms that are on OLDS sites and moves them all on NEW site where they form a molecule
    Args :
        OLDS   : Site intances. Where the atoms currently are.
        NEW    : Site instance. Where the atoms are going to form a molecule.
    """

    nb_set = NEW.neighbours_nb
    for old in OLDS:
        nb_set.update(old.neighbours_nb)
    nb_list = list(nb_set)
    site_list = list( kmc.lattice.getSite( nb ) for nb in nb_list )


    for site in site_list:
        processes_to_delete = kmc.proc_adress.get( site.conf )

        if processes_to_delete:
            for proc in processes_to_delete :
                kmc.delEvent(proc, site.number)
        else:
            writeUndefined(site.conf, filename)


    for old in OLDS:
        NEW.occupancy += 1
        old.occupancy = 0

    # safety net --------------------
    assert (NEW.occupancy < 5), 'More than 4 atoms on site'
    # -------------------------------

    for site in site_list:
        site.updateConf()
        processes_to_add = kmc.proc_adress.get( site.conf )

        if processes_to_add :
            for proc in processes_to_add :
                kmc.addEvent(proc, site.number)
        else:
            writeUndefined(site.conf, filename)



def separateMolecule(SITE, NEWS, filename):

    """
    Taking existing atoms (molecule) that are on SITE and separate them, putting them on new sites
    Args :
        SITE : Site instance. Initial site where the molecule is.
        NEWS : Site instances. Sites where the atoms are moving to (except one - the central atom -
        which is staying on SITE)
    """

    nb_set = SITE.neighbours_nb
    for new in NEWS:
        nb_set.update(new.neighbours_nb)
    nb_list = list(nb_set)
    site_list = [ kmc.lattice.getSite( nb ) for nb in nb_list ]

    for site in site_list:
        processes_to_delete = kmc.proc_adress.get( site.conf )
        if processes_to_delete:
            for proc in processes_to_delete :
                kmc.delEvent(proc, site.number)
        else :
            writeUndefined(site.conf, filename)



    for new in NEWS:
        SITE.occupancy -= 1
        new.occupancy += 1
        # safety net --------------------
        assert (new.occupancy  < 5), 'More than 4 atoms on site'
        # -------------------------------


    for site in site_list:
        site.updateConf()
        processes_to_add = kmc.proc_adress.get( site.conf )

        if processes_to_add :
            for proc in processes_to_add :
                kmc.addEvent(proc, site.number)
        else:
            writeUndefined(site.conf, filename)



def writeUndefined(number, filename):
    string = str(number) + '\n'
    found = False
    with open(filename, 'r+') as f:
        for line in f:
            if string==line:
                found=True
                break
    if not found:
        with open(filename, 'a') as f:
            f.write(string)
