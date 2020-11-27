#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""Kohonen in pure python"""

np.random.seed(0)

def l1norm(index, data):
    """Funcao que retorna a norma l1 dada a posicao `index` e o dado `data`"""
    return np.sum(np.abs(data[index] - data), axis=1)


# LINEAR
def learning_rate_linear(step, steps,
                         a, b,
                         learning_rate_start, learning_rate_end):
    if step >= steps:
        return learning_rate_end
    else:
        return a * (1.0 - step / b)


def learning_rate_linear_limits(steps, a, b):
    learning_rate_initial = a
    learning_rate_final = steps * a / (a - b)
    return learning_rate_initial, learning_rate_final


# EXPON
def learning_rate_exponential(step, steps,
                              a, b,
                              learning_rate_start, learning_rate_end):
    if step >= steps:
        return learning_rate_end
    else:
        return a * np.exp(-step/b)


def learning_rate_exponential_limits(steps, a, b):
    learning_rate_initial = a
    learning_rate_final = steps / np.log(a/b)
    return learning_rate_initial, learning_rate_final


def gaussian_neigh(step, steps, initial_radius, final_radius, lattent_space_distance):
    lmbda = (steps - 1) / np.log(initial_radius / final_radius)

    if step >= steps - 1:
        radius = final_radius
    else:
        radius = initial_radius * np.exp( step / lmbda)

    return np.exp(-0.5 * (lattent_space_distance / radius) ** 2)


#
# Initial parameters
#
nx, ny = 30, 30
max_steps = 10000
learning_rate_start = 2.0
learning_rate_end = 0.5
neigh_radius_start = 0.5
neigh_radius_end = 0.1



#
# Le dados
#
df = pd.read_csv('../inputs/well/sint02/1/training_data.csv')
logs = ['GR', 'ILD_log10', 'DeltaPHI', 'PHIND', 'PE']
data = df[logs][0:1000].values
normalized_data = (data - np.mean(data, axis=0))/np.std(data, axis=0)
data_points = normalized_data


# Define as funcoes padrao
lattent_space_distance = l1norm
neighborhood_function = gaussian_neigh
learning_rate_limit_function = learning_rate_exponential_limits
learning_rate_function = learning_rate_exponential


#
# Define topologia neuronal
#




# Cria malha
i = np.arange(nx)
j = np.arange(ny)
I, J = np.meshgrid(i, j)

# np.c_ :  Translates slice objects to concatenation along the second axis.
lattent_space = np.c_[I.ravel(), J.ravel()]


# RANDOM INITIALIZER
n_points, n_features = data_points.shape
data_min = np.min(data_points, axis=0)
data_max = np.max(data_points, axis=0)
# neurons_positions are the weights
neurons_positions = np.random.rand(nx*ny, n_features)*(data_max - data_min) + data_min


# Leaning Rate limits
learning_rate_lower, learning_rate_upper = learning_rate_limit_function(max_steps, learning_rate_start, learning_rate_end)




# Inicializa contadores de rede
step = 0
neurons = None
done = False
tol = 1.0e-6
sqerrors = []

for iteration_number in range(max_steps):
    for data_point in np.random.permutation(data_points):

        # SINGLE STEP

        # Find BMU (neuronio vencedor)
        bmu_dist = np.sum((data_point - neurons_positions)**2, axis=1)
        bmu_index = np.argmin(bmu_dist)

        # Encontra as distancias para o vencedor
        distances = lattent_space_distance(bmu_index, lattent_space)

        var =  neighborhood_function(step, max_steps,
                                     neigh_radius_start, neigh_radius_end,
                                     distances)[:, np.newaxis]
        lr = learning_rate_function(step, max_steps,
                                    learning_rate_lower, learning_rate_upper,
                                    learning_rate_start, learning_rate_end)

        # if (step >=  max_steps):
        #     print(f"UEPA STEP: {step}  ITERATION: {iteration_number}")

        displacement = lr * var * (data_point - neurons_positions)
        neurons_positions += displacement
        step += 1
        # END OF SINGLE STEP
        sqerror = np.sqrt(np.sum(displacement**2))
        if sqerror < tol:
            done = True
            break
        if np.isnan(sqerror) or np.isinf(sqerror):
            done = True
            break

    sqerrors.append(sqerror)
    print(f"Iteration {iteration_number} - sqerror: {sqerrors[-1]:0.7f} - step: {step}")
    if done:
        break


