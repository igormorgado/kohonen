import numpy as np
import numba as nb
import pandas as pd
import tensorflow as tf
tf.get_logger().setLevel('WARN')
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial.distance import cdist
from scipy.spatial import cKDTree

# TODO:
#
# Criar um metodo Tensorflow com eager variables em python direto,
# estilo numba!


# Size of Kohonen map (rows, columns)
N, M = 40, 40

# Number of features
F = 4

# Sample size
S = 697

np.random.seed(13)

# Carrega os dados sinteticos
dados_sint = pd.read_csv('inputs/dados_sint_T1.txt', delim_whitespace=True)
R = dados_sint.iloc[:, 3:].values

# Cria o mapa inicial aleatorio baseado nos valores encontrados
R_min = R.min(axis=0)
R_max = R.max(axis=0)
W = np.zeros((N,M,F))
for i in range(F):
    W[:,:,i] = np.random.random((N,M))*(R_max[i]-R_min[i])+R_min[i]


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
    """Naive numpy"""
    DELTA = np.zeros((R.shape[0],2), dtype=np.int64)
    for idx, r in enumerate(R):
        delta = np.sum((W[:,:] - r)**2, axis=2)
        DELTA[idx] = np.unravel_index(np.argmin(delta, axis=None), delta.shape)
    return DELTA


def method5(R,W):
    """Sklearn euclidean_distances"""
    R_Temp=R
    W_Temp=W.reshape(-1,W.shape[2])
    dist=euclidean_distances(R_Temp, W_Temp)
    ind_1,ind_2=np.unravel_index(np.argmin(dist,axis=1),shape=(W.shape[0],W.shape[1]))
    return np.vstack((ind_1,ind_2)).T


@nb.njit(fastmath=True,parallel=True,cache=True)
def method6(R, W):
    """Plain numba"""
    ind_i=0
    ind_j=0
    out=np.empty((R.shape[0],2),dtype=np.int64)
    for x in nb.prange(R.shape[0]):
        delta=0
        for k in range(W.shape[2]):
            delta += (R[x,k] - W[0,0,k])**2

        for i in range(W.shape[0]):
            for j in range(W.shape[1]):
                norm = 0
                for k in range(W.shape[2]):
                    norm += (R[x,k] - W[i,j,k])**2
                if norm < delta:
                    delta=norm
                    ind_i=i
                    ind_j=j
        out[x,0]=ind_i
        out[x,1]=ind_j
    return out


def method7(R,W):
    """ Scipy Cdist"""
    R_Temp=R
    W_Temp=W.reshape(-1,W.shape[2])
    dist=cdist(R_Temp, W_Temp)
    ind_1,ind_2=np.unravel_index(np.argmin(dist,axis=1),shape=(W.shape[0],W.shape[1]))
    return np.vstack((ind_1,ind_2)).T


def method8(R,W):
    # Converter W em n data points de dimensao m
    wflat = W.reshape(N * M, F)
    tree = cKDTree(wflat)
    res = tree.query(R, k=1, n_jobs=-1)[1]
    fn = lambda x: (x//N, x%N)
    return np.apply_along_axis(fn, 0, res).T


def method9(a, b):  
  """Tensorflow matrix operation"""
  # squared norms of each row in R and W
  b = tf.reshape(b, (N*N,-1))
  nr = tf.reduce_sum(tf.square(a), 1)
  nw = tf.reduce_sum(tf.square(b), 1)
  
  # na as a row and nb as a column vectors
  nr = tf.reshape(nr, [-1, 1])
  nw = tf.reshape(nw, [1, -1])

  # return pairwise euclidead difference matrix
  res = nr - 2*tf.matmul(a, b, False, True) + nw
  res = tf.argmin(res, axis=1)
  fn = lambda x: (x//N, x%N)
  #out = tf.vectorized_map(fn, res)  # SLOW
  #out = tf.map_fn(fn, res, dtype=(tf.int64, tf.int64))) # VERY SLOW
  return np.apply_along_axis(fn, 0, res).T
  #return tf.stack(out, axis=1)


def method9_nomap(a, b):  
  """Tensorflow matrix operation"""
  # squared norms of each row in R and W
  b = tf.reshape(b, (N*N,-1))
  nr = tf.reduce_sum(tf.square(a), 1)
  nw = tf.reduce_sum(tf.square(b), 1)
  
  # na as a row and nb as a column vectors
  nr = tf.reshape(nr, [-1, 1])
  nw = tf.reshape(nw, [1, -1])

  # return pairwise euclidead difference matrix
  res = nr - 2*tf.matmul(a, b, False, True) + nw
  res = tf.argmin(res, axis=1)
  return res

if __name__ == '__main__':
    print('Method 4\n', method4(R, W))
    print('Method 5\n', method5(R, W))
    print('Method 6\n', method6(R, W))
    print('Method 7\n', method7(R, W))
    print('Method 8\n', method8(R, W))
    R_tf = tf.convert_to_tensor(R)
    W_tf = tf.convert_to_tensor(W)
    print('Method 9\n', method9(R_tf, W_tf))
    print('%timeit method4(R, W)')
    print('%timeit method5(R, W)')
    print('%timeit method6(R, W)')
    print('%timeit method7(R, W)')
    print('%timeit method8(R, W)')
    print('%timeit method9(R_tf, W_tf)')
