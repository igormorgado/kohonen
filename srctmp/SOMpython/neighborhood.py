import numpy as np


class NeighborhoodFunctionBase:
    """
    Class for create a neighborhood function
    """
    def __call__(self, lattent_space_distance, step):
        raise NotImplementedError


class ThresholdNeighborhoodFunction(NeighborhoodFunctionBase):
    """
    Class for create a threshold neighborhood function
    """
    def __init__(self, threshold):
        """
        Initializer of the class

        Parameters
        ----------
        :param threshold: float

        """
        self.threshold = threshold
    
    def __call__(self, lattent_space_distance, step):
        return (lattent_space_distance <= self.threshold).astype(float)


class GaussianNeighborhoodFunction(NeighborhoodFunctionBase):
    """
    Class for create a threshold neighborhood function
    """
    def __init__(self, initial_radius, final_radius, max_steps):
        """
        Initializer of the class

        Parameters
        ----------
        :param initial_radius: float
        :param final_radius: float
        :param max_steps: float
        """
        self.lmbda = (max_steps - 1)/np.log(initial_radius/final_radius)
        self.initial_radius = initial_radius
        self.max_steps = max_steps
        self.final_radius = final_radius
    
    def __call__(self, lattent_space_distance, step):
        if step >= self.max_steps - 1:
            radius = self.final_radius
        else:
            radius = self.initial_radius*np.exp(step/self.lmbda)
        return np.exp(-0.5*(lattent_space_distance/radius)**2)
