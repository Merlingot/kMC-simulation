
#------------------------------------------------------
# File : Lattice.py
# 
# Description : Definition of the Lattice Class.
#
# Python version: 3.6.7
#------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

from site import Site



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


    def plot(self, LATTICE_PARAMETER = None, title = None, temperature = None):
        """ Plotting lattice sites """

        x = np.array([ site.coordinates[0] for site in self.sites if site.occupancy != 0])
        y = np.array([ site.coordinates[1] for site in self.sites if site.occupancy != 0])
        o = np.array([ site.occupancy for site in self.sites if site.occupancy != 0])

        # xx = np.array([ site.coordinates[0] for site in self.sites if site.occupancy == 0])
        # yy = np.array([ site.coordinates[1] for site in self.sites if site.occupancy == 0])

        if LATTICE_PARAMETER:
            x = x*LATTICE_PARAMETER*np.sqrt(3)/2
            y = y*LATTICE_PARAMETER*np.sqrt(3)/2
            xx = xx*LATTICE_PARAMETER*np.sqrt(3)/2
            yy = yy*LATTICE_PARAMETER*np.sqrt(3)/2

        fig = plt.figure(figsize = (4,4))
        if title:
            plt.title('Aire : {} m^2 \n Temperature : {} K'.format(title, temperature) )
        plt.axis('off')
        # plt.plot(xx, yy, '.', markeredgecolor='black', fillstyle='none' )
        plt.scatter(x,y, c=o, marker = '.', cmap=plt.cm.get_cmap('Blues', 4), vmin = -1, vmax = 4 )
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

