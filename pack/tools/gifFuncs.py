#######################################################
# Module: gifFuncs
# Description: contains functions to make a gif out of
# the data saved during the simulation.
# Functions included:
#    - read_data
#    - animation
#       - put_data
#       - init_anim
# Note : needs imagemagick to save the gif file.
#######################################################

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.animation import FuncAnimation
import os


def animation(coorddir, rangeFile, gifFile=None):
    """
    Function creating an animation and saving it.
    Args:
        coorddir: absolute path to the directory containing the coordinates of atoms for each kmc step
        <outdir>/coordinates/  or  <control file>.coorddir

        rangeFile: absolute path to the file containing the domain lenght
        <outdir>/range.txt  or  <control file>.rangeFile
    kwArgs:
        gifFile: absolute path, name and extension of the gif.
        <outdir>/mygif.gif  or  <control file>.gifFile
        * Will use imagemagick to save the gif
    """

    # Define custom colormap
    colors = [(1,0,0), (0,1,0)]
    customMap=matplotlib.colors.ListedColormap(colors)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    lx, ly = np.genfromtxt(rangeFile, comments = '#', unpack=True)
    ax.set_xlim([lx*(-0.1), lx*1.1])
    ax.set_ylim([ly*(-0.1), ly*1.1])
    text = ax.text(0.02, 1.0, '', transform=ax.transAxes)
    scat = ax.scatter([],[], c=[], marker = '.', cmap = customMap, vmin = 1, vmax = 4)

    def init_anim():
        text.set_text('')
        return (scat, text)

    def put_data(frame):
        scat.set_offsets(np.c_[frame[0],frame[1]])
        scat.set_array(frame[2]) #colors
        text.set_text('step={} time = {} s '.format(frame[3], frame[4]))
        return (scat, text)

    anim=FuncAnimation( fig, put_data, frames=read_data(coorddir), init_func=init_anim, interval = 300, blit = False, repeat = False)

    if gifFile:
        anim.save(gifFile, writer='imagemagick')

    return anim

def read_data(coorddir):
    """update data"""
    path, dirs, files = next(os.walk(coorddir))
    n = len(files) # number of files in coorddir
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
