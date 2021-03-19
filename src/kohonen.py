import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def som_initializer_minmax(data, nx, ny):
    """ Returns a initialized random SOM

    data = dataset to measure the limits.
    nx = number of neurons in x direction
    ny = number of neurons in y direction
    """
    data_min = np.min(data, axis=0)
    data_max = np.max(data, axis=0)
    n_points, n_features = data.shape
    W = np.random.rand(nx*ny, n_features)*(data_max - data_min) + data_min

    return W


def load_northsea():
    """ NORTH SEA DATA SET PREPROCESSING
    
    This process finishish with two variables: 
      - X_train is the data to train
      - Y_train is the target label
      - X_test is the  data to validate
      - Y_test is the  target to validate
    
    """
    df = pd.read_csv('../inputs/well/mnor/1/facies_vectors.csv')


    # NOTE(Igor): Fazer target encoding no 'NM_M' e adicionar aos data_fields
    data_fields = [ 'GR', 'ILD_log10', 'DeltaPHI', 'PHIND', 'PE' ]
    target_fields = [ 'Facies' ] 

    # NOTE(Igor) check if datafields below exist in data_fields
    data_fields_normalize = ['GR', 'ILD_log10', 'DeltaPHI', 'PHIND', 'PE' ]
    data_fields_oh_encode = []
    data_fields_t_encode = []


    ####
    #### NAO MEXO
    ####

    # Extract data
    df = df[data_fields + target_fields]

    # :-(
    df = df.dropna()

    # Apply Scaler to fields to normalize
    ct = ColumnTransformer([('df_normalization', StandardScaler(), data_fields_normalize)], remainder='passthrough')

    df = pd.DataFrame(ct.fit_transform(df), columns=df.columns)

    # Build the new field list
    all_data_fields = data_fields

    # Encode fields 
    if len(data_fields_oh_encode) > 0:
        df = pd.get_dummies(df[data_fields + target_fields], columns=data_fields_oh_encode)

        for field in data_fields_oh_encode:
            if field in all_data_fields:
                all_data_fields.remove(field)

        for field in data_fields_oh_encode:
           all_data_fields +=  list(filter(lambda v: v.startswith(field), df.columns))

    # NOTE(Igor): Build one hot encoding for FORMATION?
    X = df[all_data_fields]
    y = df[target_fields]

    return X, y


def learning_rate(k, step, max_steps):
    return k * (1.0 - step / (max_steps + 1))


def som_train(X, y, nx, ny, eta, max_steps, tol,
              initialize_function, learning_rate_function,
              verbose=False):

    n_points, n_features = X.shape

    # SOM Weights
    W = initialize_function(X.values, nx, ny)
    Wr = W.reshape(nx, ny, n_features)

    # Litology
    L = np.zeros(nx * ny)
    Lr = L.reshape(nx, ny)

    # Convergence values
    C = []

    data_points = np.c_[X, y]
    for iteration in np.arange(max_steps):
        K = learning_rate_function(eta[0], iteration, max_steps)
        K_dist = eta[1] * K

        for data_point in np.random.permutation(data_points):
            # Winner
            bmu_dist = np.sum((data_point[0:-1] - W)**2, axis=1)
            bmu_index = np.argmin(bmu_dist)

            # Update winner
            delta = (data_point[0:-1] - W[bmu_index])
            delta_lr = K * delta
            W[bmu_index] += delta_lr

            # Updata litology
            L[bmu_index] = data_point[-1]

            # Update neighboors
            # // integer division and % modulo
            bmu_row = bmu_index // ny
            bmu_col = bmu_index % ny
            bmu_coords = [ bmu_row, bmu_col ]

            up    = [(bmu_row - 1) % nx,  bmu_col          ]
            down  = [(bmu_row + 1) % nx,  bmu_col          ]
            left  = [ bmu_row,           (bmu_col - 1) % ny]
            right = [ bmu_row,           (bmu_col + 1) % ny]

            for neigh in [up, down, left, right]:
                delta_neigh = data_point[0:-1] - Wr[neigh[0],neigh[1]]
                delta_neigh_lr = K_dist * delta_neigh
                Wr[neigh[0], neigh[1]] += delta_neigh_lr
                Lr[neigh[0], neigh[1]] = data_point[-1]

        # Convergencia
        convergence_sum = 0
        for data_point in data_points:
            bmu_dist = np.sum((data_point[0:-1] - W)**2, axis=1)
            bmu_index = np.argmin(bmu_dist)

            if L[bmu_index] != data_point[-1]:
                convergence_sum += 1

        C.append(convergence_sum)

        if (verbose):
            print(f"Iteracao {iteration} - conv: {convergence_sum}")

    return W, L, C


def som_classify(X, y, W, L):

    n_points, n_features = X.shape
    clfy = np.zeros(n_points, dtype='int')

    for idx, data_point in enumerate(X):
        bmu_dist = np.sum((data_point - W)**2, axis=1)
        bmu_index = np.argmin(bmu_dist)
        clfy[idx] = L[bmu_index]

    acc = np.sum(y == clfy)/n_points

    return clfy, acc


##################################################
### MAIN
##################################################

def main():

    # Map size
    nx = 60
    ny = 60

    # learning rate 
    eta = [1, 1/1.2]

    # Simulation steps
    max_steps = 1000

    # Tolerance 
    tol = 1e-6

    seed = 42
    np.random.seed(seed)

    X, y = load_northsea()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.33, stratify=y, random_state=seed)

    W, L, C = som_train(X_train, y_train, nx, ny, eta, max_steps, tol, som_initializer_minmax, learning_rate, True)

    predict, acc = som_classify(X_test.values, y_test.values.ravel(), W, L)


if __name__ == "__main__":
    main()
