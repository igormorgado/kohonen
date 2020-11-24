import numpy as np
from matplotlib.cm import get_cmap
from matplotlib.transforms import IdentityTransform
from matplotlib.collections import PolyCollection
from utils import *

def display_hexgrid(ax, nx, ny, val, cmap, cmin=None, cmax=None):
    """
    Display an hexagonal grid in a given figure axis. This hexagonal grid represents the lattent space.

    Parameters
    ----------
    :param ax: axis object
    :param nx: int -> Number of neurons in the horizontal axis
    :param nx: int -> Number of neurons in the vertical axis
    :param val: array_like -> Position of the neurons
    :param cmap: Colormap to plot the figure

    Returns
    -------
    :return: Axis containing the hexagonal grid filled with the colormap requested
    """
    hexgrid = create_hexgrid(nx, ny)
    hexagon = create_hexagon(np.sqrt(1.0/3.0), np.pi/6.0)
    colormap = get_cmap(cmap)
    if cmin is None:
        cmin = np.min(val)
    if cmax is None:
        cmax = np.max(val)
    colors = colormap((val - cmin)/(cmax - cmin))
    collection = PolyCollection([hexagon], offsets=hexgrid, facecolors=colors, transOffset=IdentityTransform(), offset_position="data")
    ax.add_collection(collection)
    xmin = np.min(hexgrid[:,0]) - 0.5
    xmax = np.max(hexgrid[:,0]) + 0.5
    ymin = np.min(hexgrid[:,1]) - np.sqrt(1.0/3.0)
    ymax = np.max(hexgrid[:,1]) + np.sqrt(1.0/3.0)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymax, ymin)
    ax.axis('off')
    return ax


def display_rectgrid(ax, nx, ny, val, cmap, cmin=None, cmax=None):
    """
    Display a rectangular grid in a given figure axis. This hexagonal grid represents the lattent space.

    Parameters
    ----------
    :param ax: axis object
    :param nx: int -> Number of neurons in the horizontal axis
    :param nx: int -> Number of neurons in the vertical axis
    :param val: array_like -> Position of the neurons
    :param cmap: Colormap to plot the figure

    Returns
    -------
    :return: Axis containing the rectangular grid filled with the colormap requested
    """
    rectgrid = create_rectgrid(nx, ny)
    rectangle = create_rectangle(np.sqrt(1.0/2.0), np.pi/4.0)
    colormap = get_cmap(cmap)
    if cmin is None:
        cmin = np.min(val)
    if cmax is None:
        cmax = np.max(val)
    colors = colormap((val - cmin)/(cmax - cmin))
    collection = PolyCollection([rectangle], offsets=rectgrid, facecolors=colors, transOffset=IdentityTransform(), offset_position="data")
    ax.add_collection(collection)
    xmin = np.min(rectgrid[:,0]) - 0.5
    xmax = np.max(rectgrid[:,0]) + 0.5
    ymin = np.min(rectgrid[:,1]) - 0.5
    ymax = np.max(rectgrid[:,1]) + 0.5
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymax, ymin)
    ax.axis('off')
    return ax


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    ax = plt.subplot(111)
    val = np.random.rand(100)
    display_hexgrid(ax, 10, 10, val, 'hsv')
    plt.show()
