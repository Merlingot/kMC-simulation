#######################################################
# Module: saveFuncs
# Description : Module containing the functions to save
#               the data/results during the simulation.
# Functions included:
#   - writeResults
#   - writePositions
#   - writeRange
#   - saveFrames
#######################################################


import numpy as np
import matplotlib.pyplot as plt

import pack.src.kmc as kmc


def writeResults(filename, status):
    """ Writes the results of the simulation to filename to a new file."""

    with open(filename, 'w+') as resultFile:
        resultFile.write('Nombre de sites: {} \n'.format(kmc.sites_count))
        resultFile.write('Aire: {:.6f} microm. carrés \n'.format(kmc.area*1e12))
        resultFile.write('Nombre de processus: {}\n'.format(kmc.nb_of_process))
        resultFile.write('Temps initialisation (runtime): {:.6f} s.\n'.format(kmc.init_time) )
        average_time = np.mean(kmc.runtime_steps)
        resultFile.write('Temps moyen pour 1 pas kMC (runtime): {:.6f} s.\n'.format(average_time))
        resultFile.write('Temps total (runtime) : {:.6f} s. \n'.format(kmc.runtime))
        resultFile.write('Nombre de step: {} \n'.format(kmc.steps))
        resultFile.write('Temps (systeme physique) : {:.6f} microsecondes \n'.format(kmc.time*1e6))

def writeStats(filename):
    """ Writes the kmc processes statistics in % to a new file. """
    total = np.sum(kmc.process_stats)
    proc_stat = kmc.process_stats*100/total
    indexSort = np.argsort(proc_stat)
    with open(filename, 'w+') as statsFile:
        statsFile.write('# Name Type Number Occurence(%)\n')
        for index in indexSort:
            if proc_stat[index] > 0:
                statsFile.write( '{}   {}   {}   {:.5f}\n'.format( kmc.proc_list[index].name, kmc.proc_list[index].category, index, proc_stat[index] ) )

def writeRange(filename):
    """ Writes the lenght of the simulation domain to a new file."""
    with open(filename, 'w+') as rangeFile:
        rangeFile.write( '# Lx Ly\n')
        rangeFile.write( '{} {}\n'.format(kmc.lx, kmc.ly))

def writeQuickStats(filename, proc):
    """ Writes the kmc process selected at a step n. File already initiated."""
    with open(filename, 'a+') as procFile:
        procFile.write('#nStep={} Time={}\n'.format(kmc.steps, kmc.time))
        procFile.write( '{}   {}   {}   {:.0f}\n'.format( proc.name, proc.category, proc.number, kmc.process_stats[proc.number] ) )


def writePositions(filename):
    """ Writes the position of atoms and molecules to a new file
    at a specific time t and step n. The files are saved in the <out>/coordinates/ folder under the name coord_n.txt """
    with open(filename, 'w+') as posFile:
        posFile.write('#nStep={} \n'.format(kmc.steps))
        posFile.write('#Time={} \n\n'.format(kmc.time))
        for site in kmc.lattice.sites:
            if site.occupancy > 0:
                posFile.write( '{} {} {} \n'.format(site.coordinates[0], site.coordinates[1], site.occupancy) )

def saveFrames(folder, n):
    """
    Produces and save an image of the lattice after the n th kmc step.
    The image is saved in folder under the name fig_n.png.
    This is used for verification purpose.
    """

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlim(kmc.lx*(-0.1), kmc.lx*1.1)
    plt.ylim(kmc.ly*(-0.1), kmc.ly*1.1)

    xnull = [site.coordinates[0] for site in kmc.lattice.sites if site.occupancy==0]
    ynull = [site.coordinates[1] for site in kmc.lattice.sites if site.occupancy==0]

    x = [site.coordinates[0] for site in kmc.lattice.sites if site.occupancy>0]
    y = [site.coordinates[1] for site in kmc.lattice.sites if site.occupancy>0]

    plt.plot(xnull, ynull, 'ko', markersize=1, fillstyle='none')
    plt.plot(x, y, 'ro', markersize=1)

    ax.set_aspect('equal')

    if folder:
        plt.savefig( '{}fig_{}.png'.format(folder,n), format = "png", transparent = False )
    plt.close()
