#######################################################
# Executable file : creatGif.py
# Description: makes a gif from the simulation data
# How to run:
#   $ cd <simudir>
#   $ python createGif.py
#######################################################

import pack.inputs.control as ctrl
from pack.tools.gifFuncs import createGif

createGif(ctrl.coordDir, ctrl.rangeFile, ctrl.gifFile)
