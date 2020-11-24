import numpy as np


class LearningRateBase:
    """
    Class for create a Learning rate function
    """

    def __init__(self, initial_value, final_value, max_steps):
        """
        Initializer of the class

        Parameters
        ----------
        :param initial_value:  float
        :param final_value: float
        :param max_steps: float
        """
        self.initial_value = initial_value
        self.final_value = final_value
        self.max_steps = max_steps
        self.calc_parameters()
    
    def calc_parameters(self):
        raise NotImplementedError
    
    def calc_learning_rate(self, step):
        raise NotImplementedError

    def __call__(self, step):
        if step >= self.max_steps:
            return self.final_value
        else:
            return self.calc_learning_rate(step)


class LinearLearningRate(LearningRateBase):
    """
    A class for create a linear learning rate function
    """
    def calc_parameters(self):
        """
        Calcultes the parameters needed in order to calculate a linear rate function

        :return: floats -> Parameters
        """
        self.a = self.initial_value
        self.b = self.max_steps*self.initial_value/(self.initial_value - self.final_value)    
    
    def calc_learning_rate(self, step):
        """
        Calculates the linear learning rate given an specific step

        Parameters
        ----------
        :param step: int -> Step of the algorithm for calculate the current linear learning rate

        Returns
        -------
        :return: float -> Linear learning rate
        """
        return self.a*(1.0 - step/self.b)


class InverseLearningRate(LearningRateBase):
    """
    A class for create an inverse linear learning rate function
    """
    def calc_parameters(self):
        """
        Calcultes the parameters needed in order to calculate an inverse linear rate function

        :return: floats -> Parameters
        """
        self.a = self.initial_value
        self.b = self.max_steps*self.final_value/(self.initial_value - self.final_value)

    def calc_learning_rate(self, step):
        """
        Calculates the inverse linear learning rate given an specific step

        Parameters
        ----------
        :param step: int -> Step of the algorithm for calculate the current inverse linear learning rate

        Returns
        -------
        :return: float -> Inverse linear learning rate
        """

        return self.a/(1.0 + step/self.b)


class ExponentialLearningRate(LearningRateBase):
    """
    A class for create an exponential linear learning rate function
    """

    def calc_parameters(self):
        """
        Calcultes the parameters needed in order to calculate an exponential learning rate function

        :return: floats -> Parameters
        """

        self.a = self.initial_value
        self.b = self.max_steps/np.log(self.initial_value/self.final_value)

    def calc_learning_rate(self, step):
        """
        Calculates the exponential learning rate given an specific step

        Parameters
        ----------
        :param step: int -> Step of the algorithm for calculate the current exponential learning rate

        Returns
        -------
        :return: float -> Exponential learning rate
        """

        return self.a*np.exp(-step/self.b) 