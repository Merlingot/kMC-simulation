# processes.py : a script to define all processes

# imports
from pack.include.process import Process
from pack.include.procFuncs import createProcess, showConfig

# initialize list_of_processes
list_of_processes = []
list_of_processes.clear()


# Diffusion Sb4 sur la surface
list_of_processes += createProcess( "D_sb4", "diffusion", activation_energy = 60e-3, prefactor = 6e12, new_sites = 1, sym6 = True, sb4 = 0, empty = (1,2,3,4,5,6))

#  Diffusion des atomes
# 0 lien
list_of_processes += createProcess("D_a_0", 'diffusion', shell= 1,
 atoms = (0), new_sites = 1, sym6=True)
# 1 lien
lien1 = []
lien1 += createProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
 atoms = [0,1], new_sites= 2,  sym6=True)
lien1 += createProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
 atoms = [0,1], new_sites= 3,  sym6=True)
lien1 += createProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
  atoms = [0,1], new_sites= 4,  sym6=True)
lien1 += createProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
 atoms = [0,1], new_sites= 5,  sym6=True)
lien1 += createProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
 atoms = [0,1], new_sites= 6,  sym6=True)
# 2 liens
lien2  = []
lien2 += createProcess("D_a_2", 'diffusion', shell = 1,
atoms = [0,1,3], new_sites= 2,  sym6=True)
lien2 += createProcess("D_a_2", 'diffusion', shell = 1,
atoms = [0,1,3], new_sites= 4,  sym6=True)
lien2 += createProcess("D_a_2", 'diffusion', shell = 1,
atoms = [0,1,3], new_sites= 5,  sym6=True)
lien2 += createProcess("D_a_2", 'diffusion', shell = 1,
atoms = [0,1,3], new_sites= 6,  sym6=True)

# Separation de Sb4
sep=[]
# Separation 1-3-5 ou 2-4-6
sep +=  createProcess('S_135', 'molecule separation', activation_energy = 1e-3,
sb4 = 0, shell = 1,  new_sites=(0,1,3,5))
sep += createProcess('S_246', 'molecule separation', activation_energy = 1e-3,
sb4 = 0, shell = 1,  new_sites=(0,2,4,6))
# Edge Zigzag
# Edge Armchair
sep += createProcess('Sep_chaiseI', 'molecule separation',
activation_energy = 1e-3, sb4 = 0, shell=1, atoms = (15,17), new_sites=(1,4,5,6), sym6=True)


list_of_processes = list_of_processes + lien1 + lien2 + sep
