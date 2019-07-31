import kmc

def writeResults(filename, status):
  """ Writes the results of the simulation """
  with open(filename, 'w+') as resultFile:
  resultFile.write('La simulation a terminé avec un status {}\n'.format(status) )
  resultFile.write('Nombre de sites: {} \n'.format(kmc.sites_count))
  #resultFile.write('Aire: {:.6f} microm^2 \n'.format(area*1e12))
  resultFile.write('Nombre de processus: {}\n'.format(kmc.nb_of_process))
  resultFile.write('Temps initialisation (runtime): {:.6f} s.\n'.format(kmc.init_time) )
  average_time = np.mean(kmc.runtime_steps)
  resultFile.write('Temps moyen pour 1 pas kMC (runtime): {:.6f} s.\n'.format(average_time))
  resultFile.write('Temps total (runtime) : {:.6f} s. \n'.format(kmc.runtime))
  resultFile.write('Nombre de step: {} \n'.format(kmc.steps))
  resultFile.write('Temps (systeme physique) : {:.6f} s \n'.format(kmc.time))
  resultFile.write('Stats en pourcentage: \n')

  total = np.sum(kmc.process_stats)
  proc_stat = kmc.process_stats*100/total
  indexSort = np.argsort(proc_stat)
  for index in indexSort:
    if proc_stat[index] > 0: 
      resultFile.write( '{} | {} | {:.2f} \n'.format( kmc.proc_list[index].name, index, proc_stat[index] ) )

def writePositions(filename):
  	""" Writes the position of atoms and molecules to a file"""    
	with open(filename, 'w+') as posFile:
		posFile.write('# nStep: {} s. \n'.format(kmc.steps))
		posFile.write('# Time: {} s. \n\n'.format(kmc.time))
	for site in kmc.lattice.sites:
		if site.occupancy > 0:
			posFile.write( site.coordinates[0] + ' ' + site.coordinates[1] + ' ' + site.occupancy + '\n' ) 
        
        
        
        
