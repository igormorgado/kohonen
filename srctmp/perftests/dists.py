import numpy as np


# Size of Kohonen map (rows, columns)
N, M = 10, 5 

# Number of features
F = 3

# Sample size
S = 4

np.random.seed(13)
R = np.random.randint(0, 10, size=(S, F))
W = np.random.randint(-4, 5, size=(N, M, F))

# Sample random vector
#r = np.random.rand(F)

# Initial Kohonen map weights
#W = np.random.normal(loc=0.0, scale=1.0, size=(N,M,F))


## FINDING THE WINNER
# Giving the input vector and the weight matrix
def method1(r, W):
    delta = np.zeros((N,M), dtype=int)
    for i in range(N):
        for j in range(M):
            norm = 0
            for k in range(F):
                norm += (r[k] - W[i,j,k])**2
            delta[i,j] = norm
            norm = 0
    win_idx = np.unravel_index(np.argmin(delta, axis=None), delta.shape)
    return win_idx


def method2(r, W):
    delta = np.zeros((N,M), dtype=int)
    for i in range(N):
        for j in range(M):
            delta[i, j] = np.sum(((r - W[i,j])**2))
    return np.unravel_index(np.argmin(delta, axis=None), delta.shape)


def method3(r, W):
    delta = np.sum((W[:,:] - r)**2, axis=2)
    return np.unravel_index(np.argmin(delta, axis=None), delta.shape)


def method4(R, W):
    DELTA = np.zeros((R.shape[0],2))
    for idx, r in enumerate(R):
        delta = np.sum((W[:,:] - r)**2, axis=2)
        DELTA[idx] = np.unravel_index(np.argmin(delta, axis=None), delta.shape)
    return DELTA


for r in R:
    print('Method 1', method1(r, W))
    print('Method 2', method2(r, W))
    print('Method 3', method3(r, W))
                          
print('Method 4\n', method4(R, W))
