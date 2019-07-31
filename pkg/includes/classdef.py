import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

#------------------------------------------------------
# Module: process.py
# Description: definition of Process Class
#------------------------------------------------------

from pkg.utilities.constglob import EN, EMIN
from pkg.utilities.bondCounting import bond_dicts, theta


class Process:

    def __init__(self, name, category, configuration, activation_energy=None, action_sites = None, prefactor = None):
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

        self.id = None
        self.initInfo()

        ##Seulement pour la diffusion des ATOMES. On calcule l'energie d'activation avec le bond counting scheme
        if self.category == 'diffusion':
            if not self.activation_energy:
                self.calculerEnergieDiffusion()

        self.number = None
        self.rate = None

    def initInfo(self):

        bin_id = ''
        for i in self.configuration:
            bin_id += str(i)
        self.id = int(bin_id, 5) #Nombre en base 5

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
        if self.prefactor:
            return self.prefactor*np.exp(-self.activation_energy/(boltzman*temperature))
        else:
            return prefactor*np.exp(-self.activation_energy/(boltzman*temperature))

#------------------------------------------------------
# Module: lattice.py
# Description: definition of the Lattice Class.
#------------------------------------------------------

class Lattice:

    def __init__( self, sites) :
        """
        This is a list of sites
        __init__ :
            for all site self.sites :
                initializes the site.neighbours list (List(Sites))
        Arguments :
            sites (List(Sites)) : list of sites
        """
        self.sites = sites

        #Sites are ordered clockwise starting from the upright site
        # shell 1 : site.neighbours[:6]
        for site in self.sites:
            site.neighbours = [ self.getSite( i ) for i in site.neighboursNumber ]
        #shell 2 : site.neighbours[6:18]
        for site in self.sites:
            site.neighbours += [
                site.neighbours[0].neighbours[0], site.neighbours[0].neighbours[1],
                site.neighbours[1].neighbours[1], site.neighbours[1].neighbours[2],
                site.neighbours[2].neighbours[2], site.neighbours[2].neighbours[3],
                site.neighbours[3].neighbours[3], site.neighbours[3].neighbours[4],
                site.neighbours[4].neighbours[4], site.neighbours[4].neighbours[5],
                site.neighbours[5].neighbours[5], site.neighbours[5].neighbours[0]
            ]

        for site in self.sites:
            site.neighbours_nb = { neighbour.number for neighbour in site.neighbours }


    def getSite( self, number ):
        """
        Select the site with a specific id number.
        Args:
            number (int): The identifying number for a specific site.
        Returns:
            self.sites[number] (Site): The site with id number equal to 'number'
        """
        return self.sites[ number ]


    def initIds(self):
        """ Calculate the site.id for all sites on the lattice """
        for site in self.sites:
            site.id = site.identity()


#---------------------------------------------------------
# Module: site.py
# Description: definition of the Site Class.
#------------------------------------------------------

class Site:

    def __init__( self, number, coordinates, neighbours, label = None):

        """
        Initialise a lattice Site object.
        Args:
            number (Int): An identifying number for this site.
            coordinates (np.array(x,y,z)): The coordinates of this site.
            neighbours (List(Int)): A list of the id numbers of the neighbouring sites.
        Returns:
            None
        Notes:
            There should be a 1:1 mapping between sites and site numbers.
            To retrieve a Site object, you can call its number on the Lattice object

        """
        self.number = number
        self.coordinates = coordinates
        self.neighboursNumber = neighbours

        self.occupied = False
        self.occupancy = 0 # number of atoms on this site (empty=0, atom=1, Sb4=4)

        # List of neighbouring sites. Initialized in Lattice.__init__
        self.neighbours = []
        self.neighbours_nb = None

        # Configuration state of this site. Initialized in Module2.
        self.id = None


    def identity( self ):
        """
        Returns:
            the configuration id of this site
        """

        nb = str(self.occupancy)

        for i in self.neighbours:
            nb += str( i.occupancy )
            iden = int(nb, 5)
        return iden
