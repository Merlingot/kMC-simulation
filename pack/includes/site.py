#######################################################---
# Module: site.py
# Description: definition of the Site Class.
#######################################################

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
