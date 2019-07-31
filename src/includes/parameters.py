#------------------------------------------------------
# Module : parameters
# Description : functions to calculate things related to the deposition rate #               and the number of repetitions of the unit cell.
# Included functions:
#   - calculateTotalRate
#   - calculateRepetitions
#   - num
#------------------------------------------------------

from math import sqrt
from constglob import LATTICE_PARAMETER, MASS_DENSITY, AVOGADRO_NUMBER, ATOMIC_MASS

def calculateRepetitions(deposition_area):
    """ Nombres de repetition de la maille elementaire en x en y """
    unit_cell_area = 0.5*sqrt(3)*(LATTICE_PARAMETER**2)# m^2
    num = deposition_area/unit_cell_area
    Nx=int(2*num/3); Ny = int(num/3)
    return [Nx,Ny,1]

def calculateTotalRate( deposition_area, deposition_rate):
    """ Returns the rate constant for deposition in atoms/s  """
    deposition_volume = deposition_area*(deposition_rate*1e-10/60)
    return deposition_volume*MASS_DENSITY*AVOGADRO_NUMBER/ATOMIC_MASS

def num(side):
    deposition_area = side**2 #m^2
    unit_cell_area = 0.5*sqrt(3)*(LATTICE_PARAMETER**2) # m^2
    num = deposition_area/unit_cell_area
    Nx=int(2*num/3); Ny = int(num/3)
    return num, Nx, Ny
