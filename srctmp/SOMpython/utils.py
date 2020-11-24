import numpy as np


def create_hexagon(radius, phase):
    """
    Returns an hexagon with the requested radius and the requested phase shift

    Parameters
    ----------
    :param radius: float or array_like
    :param phase:  float or array_like

    Returns
    -------
    :return: 2D numpy array containing the vertices of the hexagon
    """
    theta = np.linspace(0.0, 2.0*np.pi, 6, endpoint=False) + phase
    x = radius*np.cos(theta)
    y = radius*np.sin(theta)
    hexagon = np.c_[x, y]
    return hexagon


def create_hexgrid(nx, ny):
    """
    Creates an hexagonal grid with nx horizontal cells and ny vertical cells
    Parameters
    ----------
    :param nx: float or int
    :param ny: float or int

    Returns
    -------
    :return: numpy array containing the vertices of the hexagons that make up the grid
    """
    x = np.arange(nx, dtype=float)
    y = np.arange(ny, dtype=float) * np.sqrt(3.0/4.0)
    X, Y = np.meshgrid(x, y)
    X[1::2] += 0.5
    hexgrid = np.c_[X.ravel(), Y.ravel()]
    return hexgrid


def create_rectangle(radius, phase):
    """
    Returns a square with the requested radius and the requested phase shift

    Parameters
    ----------
    :param radius: float or array_like
    :param phase:  float or array_like

    Returns
    -------
    :return: 2D numpy array containing the vertices of the square
    """
    theta = np.linspace(0.0, 2.0*np.pi, 4, endpoint=False) + phase
    x = radius*np.cos(theta)
    y = radius*np.sin(theta)
    rectangle = np.c_[x, y]
    return rectangle


def create_rectgrid(nx, ny):
    """
    Creates a rectagonal grid with nx horizontal cells and ny vertical cells
    Parameters
    ----------
    :param nx: float or int
    :param ny: float or int

    Returns
    -------
    :return: numpy array containing the vertices of the squares that make up the grid
    """
    x = np.arange(nx, dtype=float)
    y = np.arange(ny, dtype=float)
    X, Y = np.meshgrid(x, y)
    rectgrid = np.c_[X.ravel(), Y.ravel()]
    return rectgrid


def hexgrid_distance(i1, j1, i2, j2):
    x1 = j1
    y1 = i1 + (j1 + 1)//2
    z1 = i1 - j1//2
    x2 = j2
    y2 = i2 + (j2 + 1)//2
    z2 = i2 - j2//2
    dx = np.abs(x1 - x2)
    dy = np.abs(y1 - y2)
    dz = np.abs(z1 - z2)
    dist = np.max(np.stack((dx, dy, dz)), axis=1)
    return dist
