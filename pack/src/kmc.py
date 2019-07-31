#------------------------------------------------------
# Module: kmc.py
# Description: contains all the low level functions
#              needed to implement the kMC algorithm.
# Funtions included:
#	- bisection
#	- addEvent
#	- delEvent
#	- selectEvent
#	- updateCumulRate
#	- updateTime
#------------------------------------------------------

import numpy
import math
import random
import bisect


def bisection(array, value):
    """
    Finds the first element (leftmost) in 'array' that is equal or greater than 'value'.
    If 'value'= 0, finds the first element (leftmost) in 'array' that is greater than 0.
    Args :
        array (np.array) : cumulative_rates
        value (float) : random number between [ 0 and cumulative_rates[-1] )
    Returns:
        process number (Int) : process.number of the selected process
    """

    if value:
        return bisect.bisect_left(array, value)
    else:
        index = bisect.bisect_right(array, 0)
        return bisect.bisect_left(array, 0, lo = index)


def addEvent(proc_number, site_number):
    """
    Append site_number to active_sites[proc_number]
    Stores its adress in adress_list
    Updates the nb_of_sites array correspondingly
    Arg :
        proc_number : process number
        site_number : site number
    Returns:
        None
    """
    ## Safety net ##################
    assert (proc_list[proc_number].id == lattice.sites[site_number].id), 'selected event has unmatching process id and site id'
    #################################

    active_sites[proc_number].append(site_number)
    adress_list[proc_number][site_number] = len(active_sites[proc_number]) - 1
    nb_of_sites[proc_number] += 1

    ## Safety net ##################
    assert (active_sites[proc_number][adress_list[proc_number][site_number]] == site_number), 'update of adress list and active_sites after adding event is wrong'
    #################################

def delEvent(proc_number, site_number):
    """
    Removes the site_number from active_sites[proc_number]
    (Moves the last site in active_sites[proc_number] in its place)
    Update the adress list accordingly
    Updates the nb_of_sites array correspondingly
    Arg :
        proc_number : process number
        site_number : site number
    Returns:
        None
    """
    if len( active_sites[proc_number] )>1 or active_sites[proc_number][-1] != site_number:
        # verify if active_sites[proc_number] contains only 1 site
        # or if the site_number is already occupying the last slot in active_sites[proc_number].
        del_index = adress_list[proc_number][site_number]
        last_site = active_sites[proc_number][-1]
        active_sites[proc_number][del_index] = last_site
        adress_list[proc_number][last_site] = del_index
        ## Safety net ##################
        assert (active_sites[proc_number][del_index] == last_site and adress_list[proc_number][last_site] == del_index), 'updating active_sites and adress list after deleting event is wrong'
        #################################
    del active_sites[proc_number][-1]
    adress_list[proc_number][site_number] = 0
    nb_of_sites[proc_number] -= 1

def selectEvent():
    """
    Selects a process number and a site number
    Increments the process stats according to the selected process
    Args:
        None
    Returns:
        proc_number : process.number of the selected process
        site_number : site.number of the selected site
    """

    if any(cumulative_rates > 0):
        rand = random.random()*cumulative_rates[-1] #random.random() = [0,1)
        proc_number = bisection(cumulative_rates, rand)
        ## safety net ########################
        assert (active_sites[proc_number] != []), 'selected event has no active sites'
        ######################################
        process_stats[proc_number] += 1
        site_number = random.choice ( active_sites[proc_number] )
        return proc_number, site_number

    else : # this means no process can happen on the lattice anymore
        return 'stop', 'stop'


def updateCumulRate():
    """
    Calculate the cumulative sum of the rate_constants array weighted by the nb_of_sites array. Used to update cumulative_rates array.

    Note: The deposition rate is adjusted so it is always the same.
    The total deposition rate is :
        deposition rate = deposition rate per site * total number of sites
    This has to be constant. However the number of sites on which deposition can happen ( the 'active sites' ) changes during the simulation. But we want the total deposition rate to stay constant:
        deposition rate != deposition rate per site * active sites
    So the deposition rate per site has to be modified :
        modifified deposition rate per site = ( total deposition rate / active sites ) * total number of sites
    Args:
        None
    Returns:
        cumulative rates : cumulative sum of the processes rates*number of active sites for each rate (np.array)
    """
    count = numpy.sum(numpy.array([ nb_of_sites[p] for p in deposition_ids ]))
    for deposition_id in deposition_ids :
        proc_list[deposition_id].rate = total_deposition_rate*sites_count/count
    weighted_array = numpy.multiply( nb_of_sites, rate_constants )
    return numpy.cumsum(weighted_array)


def updateTime():
    """
    Calculate the simulation time for one kMC step randomly
    Used to update the time variable
    Args:
        None
    Returns :
        t: time elapsed in the physical system (float)
    """
    r = random.random()
    k = cumulative_rates[-1]
    t = -(1.0/k)*math.log(r)
    return t
