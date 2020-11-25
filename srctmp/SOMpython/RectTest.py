#!/usr/bin/env python
# coding: utf-8

# In[1]:


from neurons import *
from som import *
from learningrate import *
from neighborhood import *
from visualization import *
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv('data/training_data.csv')
logs = ['GR', 'ILD_log10', 'DeltaPHI', 'PHIND', 'PE']
data = df[logs][0:1000].values
normalized_data = (data - np.mean(data, axis=0))/np.std(data, axis=0)
normalized_data


# In[3]:


nx,ny = 30,30
startLearningRate = 2.0
endLearningRate = 0.5
maxradius = 0.5
minradius = 0.1


# In[4]:


neurons = neurons_factory_builder(nx,ny, grid = 'hexagonal', init='random')
learrning = ExponentialLearningRate(startLearningRate,endLearningRate,10000)
neighborhood = GaussianNeighborhoodFunction(0.5,0.1,10000)
som = SelfOrganizingMaps( neurons, learrning, neighborhood, normalized_data )


# In[5]:


plt.figure(figsize=(20,10))

ax1 = plt.subplot(151)
plt.title(logs[0])
display_hexgrid(ax1, nx, ny, som.neurons.positions[:,0], "hsv")


ax2 = plt.subplot(152)
plt.title(logs[1])
display_hexgrid(ax2, nx, ny, som.neurons.positions[:,1], "hsv")


ax3 = plt.subplot(153)
plt.title(logs[2])
display_hexgrid(ax3, nx, ny, som.neurons.positions[:,2], "hsv")


ax4 = plt.subplot(154)
plt.title(logs[3])
display_hexgrid(ax4, nx, ny, som.neurons.positions[:,3], "hsv")


ax5 = plt.subplot(155)
plt.title(logs[4])
display_hexgrid(ax5, nx, ny, som.neurons.positions[:,4], "hsv")

plt.show()


# In[6]:


plt.figure( figsize=(20,10) )

plt.subplot( 141 )
plt.title( str( logs[ 0 ] ) + " VS " + str( logs[ 1 ] ) )
plt.scatter( normalized_data[:,0], normalized_data[:,1] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,0], som.neurons.positions[:,1], color = 'green', label = 'Neurons')
plt.legend()

plt.subplot( 142 )
plt.title( str( logs[ 1 ] ) + " VS " + str( logs[ 2 ] ) )
plt.scatter( normalized_data[:,1], normalized_data[:,2] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,1], som.neurons.positions[:,2], color = 'green', label = 'Neurons')
plt.legend( )

plt.subplot( 143 )
plt.title( str( logs[ 2 ] ) + " VS " + str( logs[ 3 ] ) )
plt.scatter( normalized_data[:,2], normalized_data[:,3] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,2], som.neurons.positions[:,3], color = 'green', label = 'Neurons')
plt.legend( )

plt.subplot( 144 )
plt.title( str( logs[ 3 ] ) + " VS " + str( logs[ 4 ] ) )
plt.scatter( normalized_data[:,3], normalized_data[:,4] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,3], som.neurons.positions[:,4], color = 'green', label = 'Neurons')
plt.legend( )

plt.show( )


# In[ ]:


ax = plt.subplot(111)
display_hexgrid(ax, nx,ny, som.neurons.lattent_space[:,0] + som.neurons.lattent_space[:,1],'hsv')


# In[7]:


som.fit( normalized_data )


# In[8]:


plt.figure(figsize=(20,10))

ax1 = plt.subplot(151)
plt.title(logs[0])
display_hexgrid(ax1, nx, ny, som.neurons.positions[:,0], "hsv")


ax2 = plt.subplot(152)
plt.title(logs[1])
display_hexgrid(ax2, nx, ny, som.neurons.positions[:,1], "hsv")


ax3 = plt.subplot(153)
plt.title(logs[2])
display_hexgrid(ax3, nx, ny, som.neurons.positions[:,2], "hsv")


ax4 = plt.subplot(154)
plt.title(logs[3])
display_hexgrid(ax4, nx, ny, som.neurons.positions[:,3], "hsv")


ax5 = plt.subplot(155)
plt.title(logs[4])
display_hexgrid(ax5, nx, ny, som.neurons.positions[:,4], "hsv")

plt.show()


# In[9]:


plt.figure( figsize=(20,10) )

plt.subplot( 141 )
plt.title( str( logs[ 0 ] ) + " VS " + str( logs[ 1 ] ) )
plt.scatter( normalized_data[:,0], normalized_data[:,1] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,0], som.neurons.positions[:,1], color = 'green', label = 'Neurons')
plt.legend()

plt.subplot( 142 )
plt.title( str( logs[ 1 ] ) + " VS " + str( logs[ 2 ] ) )
plt.scatter( normalized_data[:,1], normalized_data[:,2] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,1], som.neurons.positions[:,2], color = 'green', label = 'Neurons')
plt.legend( )

plt.subplot( 143 )
plt.title( str( logs[ 2 ] ) + " VS " + str( logs[ 3 ] ) )
plt.scatter( normalized_data[:,2], normalized_data[:,3] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,2], som.neurons.positions[:,3], color = 'green', label = 'Neurons')
plt.legend( )

plt.subplot( 144 )
plt.title( str( logs[ 3 ] ) + " VS " + str( logs[ 4 ] ) )
plt.scatter( normalized_data[:,3], normalized_data[:,4] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,3], som.neurons.positions[:,4], color = 'green', label = 'Neurons')
plt.legend( )

plt.show( )


# In[ ]:


plt.figure(figsize=(10,10))

plt.title('UX MATRIX')
ax = plt.subplot(111)
display_hexgrid(ax, nx, ny, som.neurons.positions[:,0]  + som.neurons.positions[:,1] + som.neurons.positions[:,2]                 + som.neurons.positions[:,3] + som.neurons.positions[:,4], "hsv")


plt.show()


# In[ ]:


ax = plt.subplot(111)
display_hexgrid(ax, nx,ny, som.neurons.lattent_space[:,0] + som.neurons.lattent_space[:,1],'hsv')


# <h1> OUTRO TESTE: </h1>

# In[ ]:


df = pd.read_csv('data/training_data.csv')
logs = ['GR', 'ILD_log10', 'DeltaPHI', 'PHIND', 'PE']
data = df[logs].values
normalized_data = (data - np.mean(data, axis=0))/np.std(data, axis=0)
tdata1 = np.r_[ (-normalized_data[:,3] - 10), normalized_data[:,0] ]
tdata2 = np.r_[ -normalized_data[:,4] , normalized_data[:,1] ]
testdata = np.c_[tdata1, tdata2]


# In[ ]:


nx,ny = 9,9
startLearningRate = 4.0
endLearningRate = 1.0
maxradius = 0.5
minradius = 0.1


# In[ ]:


neurons = neurons_factory_builder(nx,ny, init='random')
learrning = LinearLearningRate(startLearningRate,endLearningRate,1000000)
neighborhood = GaussianNeighborhoodFunction(0.5,0.1,1000000)
som = SelfOrganizingMaps( neurons, learrning, neighborhood, testdata )


# In[ ]:


plt.figure(figsize=(20,10))

ax1 = plt.subplot(121)
plt.title(logs[0])
display_rectgrid(ax1, nx, ny, som.neurons.positions[:,0], "hsv")


ax2 = plt.subplot(122)
plt.title(logs[1])
display_rectgrid(ax2, nx, ny, som.neurons.positions[:,1], "hsv")


plt.show()


# In[ ]:


plt.figure( figsize=(12,10) )

plt.title( str( logs[ 0 ] ) + " VS " + str( logs[ 1 ] ) )
plt.scatter( testdata[:,0], testdata[:,1] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,0], som.neurons.positions[:,1], color = 'green', label = 'Neurons')
plt.legend()


plt.show( )


# In[ ]:


som.fit( testdata )


# In[ ]:


plt.figure(figsize=(20,10))

ax1 = plt.subplot(121)
plt.title(logs[0])
display_rectgrid(ax1, nx, ny, som.neurons.positions[:,0], "hsv")


ax2 = plt.subplot(122)
plt.title(logs[1])
display_rectgrid(ax2, nx, ny, som.neurons.positions[:,1], "hsv")


plt.show()


# In[ ]:


plt.figure( figsize=(10,10) )

plt.title( str( logs[ 0 ] ) + " VS " + str( logs[ 1 ] ) )
plt.scatter( testdata[:,0], testdata[:,1] , color = 'blue', label = 'Data')
plt.scatter( som.neurons.positions[:,0], som.neurons.positions[:,1], color = 'green', label = 'Neurons')
plt.legend()


plt.show( )


# In[ ]:


plt.figure(figsize=(10,10))

plt.title(logs[1])
ax = plt.subplot(111)
display_rectgrid(ax, nx, ny, som.neurons.positions[:,1] + som.neurons.positions[:,0], "hsv")


plt.show()


# In[ ]:




