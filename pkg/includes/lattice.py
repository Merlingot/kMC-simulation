#------------------------------------------------------
# Module: lattice.py
# Description: definition of the Lattice Class.
#------------------------------------------------------


from pkg.includes.site import Site


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
