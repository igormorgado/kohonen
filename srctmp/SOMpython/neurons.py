import numpy as np
from sklearn.decomposition import PCA
import utils as utils


class NeuronsBase:
    """
    Class for create the neurons in the lattent space
    """
    def __init__(self, nx, ny, initializer, data_points):
        """
        Initializes the neurons

        Parameters
        ----------
        :param nx: int -> Number of neurons in the horizontal axis
        :param ny: int -> Number of neurons in the vertical axis
        :param initializer: str -> Type of initializer function
        :param data_points: array_like or matrix
        """
        self.nx = nx
        self.ny = ny
        i = np.arange(nx)
        j = np.arange(ny)
        I, J = np.meshgrid(i, j)
        self.lattent_space = np.c_[I.ravel(), J.ravel()]
        self.positions = initializer(nx, ny, data_points)
    
    def lattent_space_distance(self, index):
        raise NotImplementedError


class RectangularGridNeurons(NeuronsBase):
    """
    A class for create a rectangular grid where the vertices are the neurons properties

    """
    def lattent_space_distance(self, index):
        """
        Calculates the distances between neurons using L1 distance

        Prameters
        ---------
        :param index: int -> Index of the vector input for a SOM algorithm

        Returns
        -------
        :return: array_like -> L1 distance between the indexed neuron and the rest of the grid
        """
        return np.sum(np.abs(self.lattent_space[index] - self.lattent_space), axis=1)


class HexagonalGridNeurons(NeuronsBase):
    """
    A class for create an hexagonal grid where the vertices are the neurons properties

    """
    def lattent_space_distance(self, index):
        """
        Calculates the distances between neurons using a hexagonal grid distance

        Prameters
        ---------
        :param index: int -> Index of the vector input for a SOM algorithm

        Returns
        -------
        :return: array_like -> Hexagonal grid distance between the indexed neuron and the rest of the grid
        """

        self.lattent_space = utils.create_hexgrid( self.nx, self.ny )
        i, j = self.lattent_space.T
        x = j
        y = i + (j + 1)//2
        z = i - j//2
        dx = np.abs(x - x[index])
        dy = np.abs(y - y[index])
        dz = np.abs(z - z[index])
        dist = np.max(np.stack((dx, dy, dz)), axis=0)
        return dist
        # i1 = self.lattent_space[index, 0]
        # j1 = self.lattent_space[index, 1]
        # i2 = self.lattent_space[:, 0]
        # j2 = self.lattent_space[:, 1]
        # return utils.hexgrid_distance(i1, j1, i2, j2)


def random_initializer(nx, ny, data_points):
    """
    Initializes randomly the neurons in the data points space

    Parameters
    ----------
    :param nx: int -> Number of neurons in the horizontal axis
    :param ny: int -> Number of neurons in the vertical axis
    :param data_points: Array or matrix

    Returns
    -------
    :return: array_like containing the positions of the neurons in the data space
    """

    n_points, n_features = data_points.shape
    data_min = np.min(data_points, axis=0)
    data_max = np.max(data_points, axis=0)
    return np.random.rand(nx*ny, n_features)*(data_max - data_min) + data_min


def sample_initializer(nx, ny, data_points):
    """
    Initializes the neurons in the data points space considering the spacial distribution of the data

    Parameters
    ----------
    :param nx: int -> Number of neurons in the horizontal axis
    :param ny: int -> Number of neurons in the vertical axis
    :param data_points: Array or matrix

    Returns
    -------
    :return: array_like containing the positions of the neurons in the data space
    """

    n_points, n_features = data_points.shape
    replace = nx*ny > n_points
    sample_indexes = np.random.choice(n_points, size=nx*ny, replace=replace)
    return data_points[sample_indexes]


def rectangular_grid_pca_initializer(nx, ny, data_points):
    """
    Performs a PCA before initialize the neurons in the data space

    Parameters
    ----------
    :param nx: int -> Number of neurons in the horizontal axis
    :param ny: int -> Number of neurons in the vertical axis
    :param data_points: Array or matrix

    Returns
    -------
    :return: Array_like containing the positions of the neurons in the data space
    """
    n_points, n_features = data_points.shape
    pca = PCA(n_features)
    transformed_points = pca.fit_transform(data_points)

    pc1_min = np.min(transformed_points[:,0])
    pc1_max = np.max(transformed_points[:,0])
    pc2_min = np.min(transformed_points[:,1])
    pc2_max = np.max(transformed_points[:,1])
    pc1_range = np.linspace(pc1_min, pc1_max, nx)
    pc2_range = np.linspace(pc2_min, pc2_max, ny)
    PC1, PC2 = np.meshgrid(pc1_range, pc2_range)
    pc_grid = np.zeros((nx*ny, n_features))
    pc_grid[:,0] = PC1.ravel()
    pc_grid[:,1] = PC2.ravel()

    return pca.inverse_transform(pc_grid)


def hexagonal_grid_pca_initializer(nx, ny, data_points):
    """
    Performs a PCA before initialize the neurons in the data space

    Parameters
    ----------
    :param nx: int -> Number of neurons in the horizontal axis
    :param ny: int -> Number of neurons in the vertical axis
    :param data_points: Array or matrix

    Returns
    -------
    :return: Array_like containing the positions of the neurons in the data space
    """

    n_points, n_features = data_points.shape

    pca = PCA(n_features)
    transformed_points = pca.fit_transform(data_points)

    pc1_min = np.min(transformed_points[:,0])
    pc1_max = np.max(transformed_points[:,0])
    pc2_min = np.min(transformed_points[:,1])
    pc2_max = np.max(transformed_points[:,1])
    pc1_range = np.arange(nx, dtype=float)
    pc2_range = np.linspace(pc2_min, pc2_max, ny)
    PC1, PC2 = np.meshgrid(pc1_range, pc2_range)
    PC1[1::2] += 0.5
    PC1 = PC1/(nx + 0.5)*(pc1_max - pc1_min) + pc1_min
    pc_grid = np.zeros((nx*ny, n_features))
    pc_grid[:,0] = PC1.ravel()
    pc_grid[:,1] = PC2.ravel()

    return pca.inverse_transform(pc_grid)


def neurons_factory_builder(nx, ny, grid='rectangular', init='random'):
    """
    Factory function for fabricate neurons

    Parameters
    ----------
    :param nx: int -> Number of neurons in the horizontal axis
    :param ny: int -> Number of neurons in the vertical axis
    :param grid: str -> Type of grid for create the lattent space
    :param init: str -> Type of initializer function

    Returns
    -------
    :return: method -> function for create the neurons in a given data space
    """
    if grid == 'rectangular':
        cls = RectangularGridNeurons
    elif grid == 'hexagonal':
        cls = HexagonalGridNeurons
    else:
        print("Unknown grid type '{}'. Defaulting to rectangular.".format(grid))
        cls = RectangularGridNeurons
    
    if init == 'random':
        initializer = random_initializer
    elif init == 'sample':
        initializer = sample_initializer
    elif init == 'pca':
        if cls == RectangularGridNeurons:
            initializer = rectangular_grid_pca_initializer
        else:
            initializer = hexagonal_grid_pca_initializer
    else:
        print("Unknown initializer '{}'. Defaulting to random.".format(init))
    
    def neurons_factory(data_points):
        """
        Function for create the neurons in the data space

        Parameters
        ----------
        :param data_points: array_like or matrix

        Returns
        -------
        :return: matrix containing the neurons

        """
        return cls(nx, ny, initializer, data_points)
    
    return neurons_factory
