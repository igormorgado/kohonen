import numpy as np


class SelfOrganizingMaps:
    """
    A class implementation of a Self-Organizing Maps
    """
    def __init__(self, neurons_factory, learning_rate, neighborhood_function, data_points = None):
        """
        Initializer of the class

        Parameters
        ----------
        :param neurons_factory: class or function -> Neurons comming from the function neuronsfactorybuilder
        :param learning_rate: class of function -> Learning rate comming from the LearningRateBase
        :param neighborhood_function: class or function -> Type of neighborhood comming from the NeighborhoodBase
        :param data_points: optional: array_like or matrix
        """
        self.step = 0
        #self.neurons = None
        self.neurons_factory = neurons_factory
        self.learning_rate = learning_rate
        self.neighborhood_function = neighborhood_function
        if data_points.any( ) != None:
            self.neurons = self.neurons_factory( data_points )
        else:
            self.neurons = None

    def reset(self):
        """
        Resets the neurons positions
        :return:
        """
        self.step = 0
        self.neurons = None

    def init_neurons(self, data_points):
        """
        Initialize the neurons in the data space

        Parameters
        ----------
        :param data_points: array_like or matrix

        """
        self.neurons = self.neurons_factory(data_points)

    def find_bmu(self, data_point):
        """
        Finds the best matching unit

        Parameters
        ----------
        :param data_point: array_like or matrix

        Returns
        -------
        :return: float or array
        """
        distances = np.sum((data_point - self.neurons.positions)**2, axis=1)
        return np.argmin(distances)

    def calc_displacement(self, data_point, step):
        """
        Calculates the displacement of the neurons in both data and lattent space

        Parameters
        ----------
        :param data_point: array_like or matrix
        :param step: int -> Current step of the algorithm

        Returns
        -------
        :return: float -> The displacement of the neurons
        """
        bmu_index = self.find_bmu(data_point)
        distances = self.neurons.lattent_space_distance(bmu_index)
        var =  self.neighborhood_function(distances, step)[:,np.newaxis]
        displacement = self.learning_rate(step) * var * (data_point - self.neurons.positions)
        return displacement

    def single_step(self, data_point):
        """
        Performs a single step moving the neurons

        Parameters
        ----------
        :param data_point: array_like or matrix

        Returns
        -------
        :return: float -> The displacement of tha current step
        """
        displacement = self.calc_displacement(data_point, self.step)
        self.neurons.positions += displacement
        self.step += 1
        return displacement

    def fit(self, data_points, max_iterations=10000, tolerance=1.0E-6):
        """
        Performs the fit of the neurons with the data

        Parameters
        ----------
        :param data_points: array_like or matrix
        :param max_iterations: float or int
        :param tolerance: float or int

        """
        self.reset()
        self.init_neurons(data_points)
        done = False
        for iteration_number in range(max_iterations):
            for data_point in np.random.permutation(data_points):
                displacement = self.single_step(data_point)
                sqerror = np.sqrt(np.sum(displacement**2))
                if sqerror < tolerance:
                    done = True
                    break
            print(f"Iteration {iteration_number} - sqerror : {sqerror:0.7f} - step: {self.step}")
            if done:
                break
