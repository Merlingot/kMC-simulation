#Function: doSteps
#Description: Function needed to run n kmc steps


import time

import kmc
from runProc import decisionTree


def doSteps( n, undefinedFile, posFile, TOTAL_DEPOSITON_RATE )
    
    Performs n kMC step.
    Args
        n (int) : Number of kMC steps to run
	undefinedFile (str) : file name to write undefined configurations
	posFile (str) : file name to write coordinates of atoms
	TOTAL_DEPOSITON_RATE (float) : total deposition rate
    Returns
        stop (Bool) : indicates if the simulation had to be stopped 
	       	      before the n steps were completed due to some reason. 
    
    steps_done = 0
    stop = False
    while steps_done < n 

        t0 = time.clock()

        selected_process_nb, selected_site_nb = kmc.selectEvent()

        if selected_process_nb :

            PROC = kmc.proc_list[ selected_process_nb ]
            SITE = kmc.lattice.getSite( selected_site_nb )

            #safety net -----------------------------------
            assert (PROC.id == SITE.id), 'unmatching event has been selected'
            #----------------------------------------------

            decisionTree(PROC, SITE, undefinedFile)

            kmc.time += kmc.updateTime()
            kmc.cumulative_rates = kmc.updateCumulRate(total_dep_rate)

            t1 = time.clock()
            kmc.runtime_steps.append(t1-t0) 
            kmc.runtime_time += t1-t0
			
	    steps_done += 1
            kmc.steps += 1

        else: 
            stop = True
            break

    return stop

