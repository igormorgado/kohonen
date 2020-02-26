import numpy as np
import pandas as pd
import zarr
import xarray
import timeit
import tensorflow as tf


ARR = np.arange(1e8)
ARR = ARR.reshape(10000,10000)

ZARR = zarr.array(ARR, chunks=(1000,1000))
PARR = pd.DataFrame(ARR, index=ARR[:,0])
XARR = xarray.DataArray(ARR)
LARR = list(ARR)
TARR = tf.convert_to_tensor(ARR)

print('''%timeit n = np.random.randint(8000); ARR[n:n+1000]''')
print('''%timeit n = np.random.randint(8000); LARR[n:n+1000]''')
print('''%timeit n = np.random.randint(8000); XARR[n:n+1000]''')
print('''%timeit n = np.random.randint(8000); PARR.iloc[n:n+1000]''')
print('''%timeit n = np.random.randint(8000); ZARR[n:n+1000]''')
print('''%timeit n = np.random.randint(8000); TARR[n:n+1000]''')

