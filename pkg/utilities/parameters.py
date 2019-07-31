#------------------------------------------------------
# Module : parameters
# Description : functions to calculate things related to the deposition rate #
# Included functions:
#   - calculateTotalRate
#   - calculateDepositionArea
# Unit cell dimensions : [0,0] to [a/2, 2*a/sqrt(3)]
#------------------------------------------------------


from math import sqrt
from pkg.utilities.const import LATTICE_PARAMETER, MASS_DENSITY, AVOGADRO_NUMBER, ATOMIC_MASS

def calculateTotalRate( deposition_area, deposition_rate):
    """ Returns the rate constant for deposition in atoms/s  """
    deposition_volume = deposition_area*(deposition_rate*1e-10/60)
    return deposition_volume*MASS_DENSITY*AVOGADRO_NUMBER/ATOMIC_MASS

def calculateDepositionArea(Nx, Ny):
    """ Returns the deposition area in m^2 """
    Lx = Nx*LATTICE_PARAMETER
    Ly = Ny*LATTICE_PARAMETER*3/sqrt(3)
    return Lx*Ly, Lx, Ly
