#------------------------------------------------------
# Module: gifFuncs
# Description: contains functions to make a gif out of
# the frames saved during the simulation.
# Functions included:
#    - animation
#    - read_data
#    - set_data
#------------------------------------------------------

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animation(coordDir, rangeFile, gifFile):
    """
    Function creating an animation and saving it.
    Args:
        coordDir: absolute path to the directory containing the frames (frame = file containing the coordinates of atoms for each kmc step)
        <packdir>/pack/out/coordinates/ or <control file>.coordDir

        rangeFile: absolute path to the file containing the domain lenght
        <packdir>/pack/out/range.txt or <control file>.rangeFile

        gifFile: absolute path, name and extension of the gif.
        <packdir>/pack/out/<name>.gif or <control file>.gifFile
    """

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # read rangeFile to retrieve domain lenght and set xlims and ylim
    lx, ly =
    plt.xlim(lx*(-0.1), lx*1.1)
    plt.ylim(ly*(-0.1), ly*1.1)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    scat = ax.scatter([],[], c=[], marker = '.', markersize=1, cmap=plt.cm.get_cmap('Blues', 4), vmin = -1, vmax = 4)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    time_text.set_text('')

    # read dataFolder
    # number of files in coordDir
    nb_of_files =

    anim=FuncAnimation( fig, set_data, frames=read_data(nb_of_files), interval = 300, blit = True, repeat = False)

    # save gif
    save( '{}'.format(gifFile))


def read_data(n):
    """update data"""
    i=0
    while i < n:
        # open file

        # retrieve data
        time =
        x, y, occ =
        yield x, y, occ, time, step
        i+=1

def set_data(frame):
    """set data to scatter plot"""
    scat.set_array(frame[2])
    scat.set_offsets(np.c_[frame[0],frame[1]])
    text.set_text('time = {:.6f} \n step = {}'.format(frame[3], frame[4]))
    return scat, text
