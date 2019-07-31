"""processes.py : a script to define all processes
"""

from DataTypes import *
list_of_processes = []
list_of_processes.clear()

# ============================= Diffusion ======================================

# Diffusion Sb4 sur la surface -------------------------------------------------
#Tous les cas possibles de diffusion de Sb4:
list_of_processes += generateProcess( "D_sb4", "diffusion", activation_energy = 60e-3,
prefactor = 6e12, new_sites = 1, sym6 = True, sb4 = 0, empty = (1,2,3,4,5,6))

#  Diffusion des atomes ---------------------------------------------------------
# 0 lien
list_of_processes += generateProcess("D_a_0", 'diffusion', shell= 1,
 atoms = (0), new_sites = 1, sym6=True)
# 1 lien
lien1 = []
lien1 += generateProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
 atoms = [0,1], new_sites= 2,  sym6=True)
lien1 += generateProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
 atoms = [0,1], new_sites= 3,  sym6=True)
lien1 += generateProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
  atoms = [0,1], new_sites= 4,  sym6=True)
lien1 += generateProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
 atoms = [0,1], new_sites= 5,  sym6=True)
lien1 += generateProcess("D_a_1", 'diffusion', empty = [2,3,4,5,6],
 atoms = [0,1], new_sites= 6,  sym6=True)
# 2 liens
lien2  = []
lien2 += generateProcess("D_a_2", 'diffusion', shell = 1,
atoms = [0,1,3], new_sites= 2,  sym6=True)
lien2 += generateProcess("D_a_2", 'diffusion', shell = 1,
atoms = [0,1,3], new_sites= 4,  sym6=True)
lien2 += generateProcess("D_a_2", 'diffusion', shell = 1,
atoms = [0,1,3], new_sites= 5,  sym6=True)
lien2 += generateProcess("D_a_2", 'diffusion', shell = 1,
atoms = [0,1,3], new_sites= 6,  sym6=True)
# # ==============================================================================


# # =========================== Separation de Sb4 ================================
sep=[]
# Separation 1-3-5 ou 2-4-6
sep +=  generateProcess('S_135', 'molecule separation', activation_energy = 1e-3,
sb4 = 0, shell = 1,  new_sites=(0,1,3,5))
sep += generateProcess('S_246', 'molecule separation', activation_energy = 1e-3,
sb4 = 0, shell = 1,  new_sites=(0,2,4,6))

# Proche du domaine ------------------------------------------------------------
# Edge Zigzag

# b = generateProcess('Separation Sb4 zigzag A', 'molecule separation', activation_energy = 1e-2, sb4 = 0, shell=1,
# unid = (16,10), atoms = (12,13,14), new_sites=(0,1,3,5))

# Edge Armchair
sep = generateProcess('Sep_chaiseI', 'molecule separation',
activation_energy = 1e-3, sb4 = 0, shell=1, atoms = (15,17), new_sites=(1,4,5,6), sym6=True)
# ========================================================================

list_of_processes = list_of_processes + lien1 + lien2 + sep
