#######################################################
# Module: process.py
# Description: definition of Process Class
#######################################################


import numpy as np

from pack.utilities.const import EN, EMIN
from pack.utilities.bondCounting import bond_dicts, theta


class Process:

    def __init__(self, name, category, configuration, activation_energy=None, action_sites = None, prefactor = None, rate=None):
        """
        Args:
            name (Str)    :  process name
            category (Str): 'diffusion', 'molecule separation', 'molecule creation',  'evaporation' or 'deposition'
            configuration (list)
        KArgs:
            activation_energy (Float) : activation energy for this process (eV)
            action sites (tuple / tuple(tuple)), optionnal, default to None
            prefactor (Float)
        """
        self.name = name
        self.category = category
        self.configuration = configuration

        self.activation_energy = activation_energy
        self.action_sites = action_sites
        self.prefactor = prefactor

        self.rate=rate

        self.number = None
        self.conf = None
        self.initInfo()

        ##Seulement pour la diffusion des ATOMES. On calcule l'energie d'activation avec le bond counting scheme
        if self.category == 'diffusion':
            if not self.activation_energy:
                self.calculerEnergieDiffusion()


    def initInfo(self):

        bin_id = ''
        for i in self.configuration:
            bin_id += str(i)
        self.conf = int(bin_id, 5) #Nombre en base 5

    def calculerEnergieDiffusion(self):

        n = self.action_sites
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


    def calculateRate(self, prefactor, temperature, boltzman):
        """ calculates a process rate
        prefactor : (default from parameters.py)
            - uses the process.prefactor if it has one
            - else : uses the default prefactor (the one in the argument)
        temperature : from parameters.py
        boltzman : from parameters.py
        """
        if self.rate == None:
            if self.prefactor:
                return self.prefactor*np.exp(-self.activation_energy/(boltzman*temperature))
            else:
                return prefactor*np.exp(-self.activation_energy/(boltzman*temperature))
        else:
            return self.rate
