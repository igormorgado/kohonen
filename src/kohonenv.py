import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Esta implementação de Kohonen é identica a realizada pelo Vitor em
# kohonen.f95. 
#
# Nenhuma otimização deve ser realizada neste arquivo que deve manter sempre a
# mesma logica e algoritmo da implementacao referencia em Fortran.


# TODO(IGor): Separar o target do dado...
# df_t1 = pd.read_csv('../inputs/well/sint01/1/dados_sint_T1.txt', sep='[\s,]{2,20}', engine='python')
# 
# # NOTA (IGor): O ultimo campo deve SEMPRE ser o `codigo`
# data_fields = ['dens', 'gama', 'rho', 'vel', 'codigo' ]

df = pd.read_csv('../inputs/well/mnor/1/mardonorte_treinamento.txt', sep='\s', engine='python')
data_fields = ['GR', 'ILD_log10', 'DeltaPHI', 'PHIND', 'Facies' ]


# Dado de entrada deve ser um numpy array
# Dado de target deve ser um numpy array



tr = df[data_fields].values
data_min = np.min(tr, axis=0)
data_max = np.max(tr, axis=0)
data_points = tr



nx = 60
ny = 60

n_points, n_features = tr.shape

print(f"Numero de neuronios na rede: {nx * ny}")


# Inicializa aleatorio baseado nos limites do datdo
neurons_positions = np.random.rand(nx*ny, n_features)*(data_max - data_min) + data_min
neurons_positions[:,n_features - 1] = 0.0
a = neurons_positions
w = neurons_positions



def learning_rate(k, step, max_steps):
    return k * (1.0 - step / (max_steps + 1))


#np.random.seed(0)
max_steps = 1000
W = neurons_positions.reshape(nx, ny, n_features)
K_factor = 1/1.2
convergencia  = []
converror = []
tol = 1e-9
done = False

for iteracao in np.arange(max_steps):
    K = learning_rate(1.0, iteracao, max_steps)
    K_dist = K_factor * K

    for data_point in np.random.permutation(data_points):

        #
        # Neuronio vencedor
        #
        # NOTA (IGor): Nunca devemos utilizar o campo final (codigo) para o 
        # calculo das distancias 
        bmu_dist = np.sum((data_point[0:-1] - neurons_positions[:,0:-1])**2, axis=1)
        bmu_index = np.argmin(bmu_dist)

        #
        # Update do neuronio vencedor
        #

        # Do not update the last feature (category: litology) - discrete update
        delta = (data_point[0:-1] - neurons_positions[bmu_index][0:-1])
        delta_lr = K * delta

        neurons_positions[bmu_index][0:-1] += delta_lr

        error = delta_lr ** 2

        # Update litology
        neurons_positions[bmu_index][-1] = data_point[-1]

        #
        # Update vizinhos
        #

        # // integer division and % modulo
        bmu_row = bmu_index // ny
        bmu_col = bmu_index % ny
        bmu_coords = [ bmu_row, bmu_col ]

        up    = [(bmu_row - 1) % nx,  bmu_col          ]
        down  = [(bmu_row + 1) % nx,  bmu_col          ]
        left  = [ bmu_row,           (bmu_col - 1) % ny]
        right = [ bmu_row,           (bmu_col + 1) % ny]

        for neigh in [up, down, left, right]:
            delta_neigh = data_point[0:-1] - W[neigh[0],neigh[1]][0:-1]
            delta_neigh_lr = K_dist * delta_neigh
            W[neigh[0], neigh[1]][0:-1] += delta_neigh_lr
            W[neigh[0], neigh[1]][-1] = data_point[-1]
            error += delta_neigh_lr ** 2


        
        #Criterio de parada
        
        error = np.sum(error)
        converror.append(error)
        # if error < tol:
        #     done = True
        #     break




    #
    # Convergencia
    #
    somacon = 0
    for data_point in data_points:
        bmu_dist = np.sum((data_point[0:-1] - neurons_positions[:,0:-1])**2, axis=1)
        bmu_index = np.argmin(bmu_dist)

        if neurons_positions[bmu_index][-1] != data_point[-1]:
            somacon += 1

    print(f"Iteracao {iteracao} - error: {error}")
    convergencia.append(somacon)
    if done:
        break


#
# Classificacao de um dado / teste de validacao
#

df_t1 = pd.read_csv('../inputs/well/mnor/1/mardonorte_validacao.txt', sep='\s', engine='python')
data_fields = ['GR', 'ILD_log10', 'DeltaPHI', 'PHIND', 'Facies' ]

# df_c1 = pd.read_csv('../inputs/well/sint01/1/dados_sint_c1.txt', sep='[\s,]{2,20}', engine='python')
# data_fields = ['dens', 'gama', 'rho', 'vel', 'codigo' ]

cl = df_t1[data_fields].values
n_points, n_features = cl.shape

classificacao = np.zeros(n_points, dtype='int')
poco = cl[:, -1].copy().astype('int')

for idx, data_point in enumerate(cl):
    bmu_dist = np.sum((data_point[0:-1] - neurons_positions[:,:-1])**2, axis=1)
    bmu_index = np.argmin(bmu_dist)
    classificacao[idx] = neurons_positions[bmu_index][-1] 

# Acuracia
acuracia = np.sum(poco == classificacao)/len(poco)
print(f"Acuracia: {acuracia}")


# Grafico de classificacao do poco
osdois = np.c_[poco,classificacao]
osdois [osdois > 400] -= 440

fig, ax = plt.subplots()
plt.imshow(osdois, aspect=.01, interpolation='none')


# Grafico de atribuitos
fig, ax = plt.subplots(nrows=1, ncols=n_features)
for idx, feat in enumerate(data_fields):
    data = neurons_positions.reshape(nx, ny, n_features)[:,:,idx]
    msh = ax[idx].matshow(data)
    ax[idx].set_title(data_fields[idx])
    fig.colorbar(msh, ax=ax[idx])


# Graf error
convsrt =int(len(converror)/len(convergencia))
erravg = []
for i in range(len(converror)//convsrt):
    val = np.mean(converror[i*convsrt:(i+1)*convsrt])
    erravg.append(val)

fig, ax = plt.subplots()
errcolor = 'tab:red'
#ax.plot(converror[::int(convsrt)], color=errcolor, alpha=.5)
ax.plot(erravg, color=errcolor, alpha=.5)
ax.tick_params(axis='y', labelcolor=errcolor)
ax.set_ylabel('Erro', color=errcolor)
ax.set_xlabel('Iteration')
convcolor = 'tab:blue'
ax2 = ax.twinx()
ax2.plot(convergencia, color=convcolor, alpha=.5)
ax2.tick_params(axis='y', labelcolor=convcolor)
ax2.set_ylabel('Converrgencia', color=convcolor)




