#######################################################
# Module: process.py
# Description: definition of Process parent and child
# classes
#######################################################


import numpy as np

from pack.utilities.const import EN, EMIN, PREFACTOR
from pack.utilities.bondCounting import bond_dicts, theta

class Process:
    """Parent class of all processes class"""

    def __init__(self, name, category, configuration):
        """
        Args:
            name (Str)    :  process name
            category (Str): 'diffusion', 'molecule separation', 'molecule creation',  'evaporation' or 'deposition'
            configuration (list)
        """
        self.name = name
        self.category = category
        self.configuration = configuration

        self.rate=None

        self.number = None
        self.conf = None
        self.initInfo()

    def initInfo(self):
        bin_id = ''
        for i in self.configuration:
            bin_id += str(i)
        self.conf = int(bin_id, 5) #Nombre en base 5


class Deposition( Process ):

    def __init__(self, name, category, configuration, rate) :

        Process.__init__(self, name, category, configuration)
        self.rate=rate


class Evaporation( Process ):

    def __init__(self, name, category, configuration, activation_energy=None, prefactor=PREFACTOR) :

        Process.__init__(self, name, category, configuration)
        if not self.activation_energy:
            self.calculateEE()

    def calculateRate(self, temperature, boltzman):
        self.rate = self.prefactor*np.exp(-self.activation_energy/(boltzman*temperature))

    def calculateEE(self):
        for n in range(1,6):
            nB += self.configuration[n]
        self.activation_energy= 0.5*EN + nB*EN



class Diffusion(Process):

    def __init__(self, name, category, configuration, action_sites, activation_energy=None, prefactor=PREFACTOR) :

        Process.__init__(self, name, category, configuration)
        self.next_site = action_sites
        self.activation_energy=activation_energy
        self.prefactor=prefactor

        if not self.activation_energy:
            self.calculateDE()

    def calculateRate(self, temperature, boltzman):
        self.rate = self.prefactor*np.exp(-self.activation_energy/(boltzman*temperature))

    def calculateDE(self):

        n = self.next_site
        c = self.configuration

        ni_par = c[ bond_dicts[n]['niA'] ]
        nf_par = c[ bond_dicts[n]['nfA'] ]
        ni_per = 0
        for i in bond_dicts[n]['niE']:
            ni_per += c[i]
        nf_per = 0
        for i in bond_dicts[n]['nfE']:
            nf_per += c[i]

        nB = ni_par + (ni_per - nf_per)*theta(ni_per - nf_per)
        nR = np.min( np.array([ni_per, nf_per]) )
        nG_per = (nf_per - ni_per)*theta(nf_per-ni_per)
        nG_par = nf_par

        E = EN/2 + nB*EN + nR*(EN/2) - nG_per*(EN/4) - nG_par*(EN/8)
        if E < 0:
            E = EMIN
        self.activation_energy = E

class MolCreation( Process ):

    def __init__(self, name, category, configuration, action_sites, rate=None, activation_energy=None, prefactor=PREFACTOR):

        Process.__init__(self, name, category, configuration)
        self.rate=rate
        self.mol_site = action_sites[1]
        self.atom_sites = action_sites[0]
        self.activation_energy=activation_energy
        self.prefactor=prefactor

    def calculateRate(self, temperature, boltzman):
        self.rate = self.prefactor*np.exp(-self.activation_energy/(boltzman*temperature))


class MolDissociation( Process ):

    def __init__(self, name, category, configuration, action_sites, rate=None, activation_energy=None, prefactor=PREFACTOR):

        Process.__init__(self, name, category, configuration)
        self.rate=rate
        self.atom_sites = action_sites
        self.activation_energy=activation_energy
        self.prefactor=prefactor

    def calculateRate(self, temperature, boltzman):
        self.rate = self.prefactor*np.exp(-self.activation_energy/(boltzman*temperature))
