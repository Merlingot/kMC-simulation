#######################################################
# Executable file : do_animation.py
# Description: makes a gif from the simulation data
# How to run:
#   $ cd <simudir>
#   $ python do_animation.py
#######################################################


import pack.inputs.control as ctrl
from pack.tools.animFuncs import animationFunc

animationFunc(ctrl.coorddir, ctrl.rangeFile, ctrl.gifFile)
