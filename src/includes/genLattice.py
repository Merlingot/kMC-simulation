# Function: createLattice
# Description: function to create a Lattice Class instance


import numpy as np

#PROBLEMS
from latticeClass import Lattice
from siteClass import Site


def createLattice( repetitions ):
    """
    Generate all Sites, then create the Lattice.
    Args:
        repetitions (Tuple(x,y,z)): tuple of the number of repetitions along the 3 axis for the simulation cell.
            x (Int):           Number of lattice repeat units along x.
            y (Int):           Number of lattice repeat units along y.
            z (Int):           Number of lattice repeat units along z.

    Returns:
        Lattice(sites)
    """

    x, y, z = repetitions[0], repetitions[1], 1 # 2D

    grid = np.array( list( range( 0, int( x * y * z * 6  ) ) ) ).reshape( x, y, z, 6, order='C' )

    sites = []

    for k in range(z):
        for i in range( x ):
            for j in range( y ):
        # site 1
                site1 = np.array( [0.0 , 0.0 , 0.0 ] )
                r1 = site1 + np.array( [i*sqrt(3), j*3, k] )
                n1 = grid[i, j, k, 0]
                nb1 = [
                    grid[i,j,k,4] ,
                    grid[i,j,k,1] ,
                    np.roll( grid, +1, axis=1)[i,j,k,5],
                    np.roll( grid, +1, axis=1 )[i,j,k,3],
                    np.roll( grid, (+1,+1), axis=(0,1) )[i,j,k,5],
                    np.roll( grid, +1, axis=0 )[i,j,k,1]
                ]
                sites.append(Site(n1, r1, nb1))
        # site 2
                site2 = np.array( [sqrt(3)/2, 1/2, 0.0] )
                r2 = site2 + np.array( [i*sqrt(3), j*3, k] )
                n2 = grid[i, j, k, 1]
                nb2 = [
                    grid[i,j,k,2],
                    np.roll( grid, -1, axis=0 )[i,j,k,4] ,
                    np.roll( grid, -1, axis=0 )[i,j,k,0] ,
                    np.roll( grid, +1, axis=1 )[i,j,k,5] ,
                    grid[i, j, k, 0] ,
                    grid[i, j, k, 4]
                ]
                sites.append(Site(n2, r2, nb2))
        # site 3
                site3 = np.array( [sqrt(3)/2, 3/2 , 0.0 ] )
                r3 = site3 + np.array( [i*sqrt(3), j*3, k] )
                n3 = grid[i, j, k, 2]
                nb3 = [
                    grid[i,j,k,5],
                    np.roll( grid, -1, axis=0 )[i,j,k,3],
                    np.roll( grid, -1, axis=0 )[i,j,k,4],
                    grid[i,j,k,1],
                    grid[i,j,k,4],
                    grid[i,j,k,3]
                ]
                sites.append(Site(n3, r3, nb3))
        # site 4
                site4 = np.array( [0.0, 2 , 0.0] )
                r4 = site4 + np.array( [i*sqrt(3), j*3, k] )
                n4 = grid[i, j, k, 3]
                nb4 = [
                    np.roll( grid, -1, axis=1 )[i,j,k,0],
                    grid[i,j,k,5],
                    grid[i,j,k,2],
                    grid[i,j,k,4],
                    np.roll( grid, +1, axis=0 )[i,j,k,2],
                    np.roll( grid, +1, axis=0 )[i,j,k,5]
                ]
                sites.append(Site(n4, r4, nb4))
        #site 5
                site5 = np.array([0.0 , 1, 0.0])
                r5 = site5 + np.array( [i*sqrt(3), j*3, k] )
                n5 = grid[i, j, k, 4]
                nb5 = [
                    grid[i,j,k,3],
                    grid[i,j,k,2],
                    grid[i,j,k,1],
                    grid[i,j,k,0],
                    np.roll( grid, +1, axis=0 )[i,j,k,1],
                    np.roll( grid, +1, axis=0 )[i,j,k,2]
                ]
                sites.append ( Site (n5, r5, nb5) )
        #site 6
                site6 = np.array([sqrt(3)/2 , 2.5 , 0.0])
                r6 = site6 + np.array( [i*sqrt(3), j*3, k] )
                n6 = grid[i, j, k, 5]
                nb6 = [
                    np.roll( grid, -1, axis=1 )[i,j,k,1],
                    np.roll( grid, (-1,-1), axis=(0,1) )[i,j,k,0],
                    np.roll( grid, -1, axis=0 )[i,j,k,3],
                    grid[i,j,k,2],
                    grid[i,j,k,3],
                    np.roll( grid, -1, axis = 1)[i,j,k,0]
                ]
                sites.append ( Site (n6, r6, nb6) )

    return Lattice(sites)
