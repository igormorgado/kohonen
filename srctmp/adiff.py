import sys
import jax.numpy as jnp
import numpy as np
from jax import grad, jit, vmap
from jax import random

key = random.PRNGKey(0)

size = 3000
x = random.normal(key, (size, size), dtype=jnp.float32)
y = np.random.randn(size,size).astype(np.float32)

%timeit jnp.dot(x, x.T).block_until_ready()
%timeit np.dot(y, y.T)
