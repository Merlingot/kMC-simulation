#######################################################
# Module: gifFuncs
# Description: contains functions to make a gif out of
# the data saved during the simulation.
# Functions included:
#    - read_data
#    - animation
#       - put_data
#       - init_anim
#######################################################

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import os

def animation(coordDir, rangeFile, gifFile):
    """
    Function creating an animation and saving it.
    Args:
        coordDir: absolute path to the directory containing the coordinates of atoms for each kmc step
        <outdir>/coordinates/  or  <control file>.coordDir

        rangeFile: absolute path to the file containing the domain lenght
        <outdir>/range.txt  or  <control file>.rangeFile

        gifFile: absolute path, name and extension of the gif.
        <outdir>/mygif.gif  or  <control file>.gifFile
    """
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    lx, ly = np.genfromtxt(rangeFile, comments = '#', unpack=True)
    ax.set_xlim([lx*(-0.1), lx*1.1])
    ax.set_ylim([ly*(-0.1), ly*1.1])
    text = ax.text(0.02, 1.0, '', transform=ax.transAxes)

    line, = ax.plot([], [], 'o', markersize=1)

    def init_anim():
        line.set_data([], [])
        text.set_text('')
        return (line, text)

    def put_data(frame):
        line.set_data(frame[0],frame[1])
        text.set_text('step={} time = {} s '.format(frame[3], frame[4]))
        return (line, text)

    anim=FuncAnimation( fig, put_data, frames=read_data(coordDir), init_func=init_anim, interval = 500, blit = False, repeat = False)

    plt.show()

    return anim

def read_data(coordDir):
    """update data"""
    path, dirs, files = next(os.walk(coordDir))
    n = len(files) # number of files in coordDir
    i=0
    while i < n:
        file = path+'step_{}.txt'.format(i+1)
        x, y, occ = np.genfromtxt(file, comments='#', unpack=True)
        with open( file, 'r') as f:
            line1 = f.readline()
            line2 = f.readline()
        nstep = line1[7:]
        time = line2[6:]
        i+=1
        yield x, y, occ, nstep, time
