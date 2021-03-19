# Kohonen

Este repositório é o conjunto de esforços para o uso do modelo de Kohonen de
classificação de uma rede neuronal aplicada a identificação de litografias.

O objetivo deste trabalho é a identificação do melhor conjunto de atributos
para a classificação. Inicialmente o método aplicado será o uso de algoritmos
genéticos multi objetivos utilizando o modelo de Kohonen como função
custo.

Compativel com Python >= 3.5 

## Criando o diretorio de projeto

1. Crie o diretorio virtual

```
python3 -m venv  venv
```

2. Ative o diretorio virtual

```
source venv/bin/activate
```

3. Instale os requisitos

```
pip3 install -r requirements.txt
```

4. (opcional) Instale os requisitos de desenvolvimento

```
pip3 install -r requirements-dev.txt
```

5. (opcional) Instalar os requisitos do tensorflow. 

```
pip3 install -r requirements-tf.txt
```

TODO: Verificar os codigos do tensorflow.

## Macetes para instalação 

1. Tensorflow necessita de python3.5 ao 3.8, não funcionara com outras versoes.

2. TotalDepth necessita de llvm9 ou 10 


### No debian-buster

O default do debian-buster é python3.9 e llvm11. Deve-se instalar as versoes
diretamente e chamar os binarios de acordo.

```
sudo apt install python3.8-venv  python3.8-dev
```

```
sudo apt purge llvm llvm-runtime
ln -s /usr/bin/llvm-config  /usr/lib/llvm10/bin/llvm-config
```

Realizar a instalacao do ambiente virtual da descrição acima,  utilizando
python3.8 ao inves de python3 ou python.

## Suport à GPU

Instalar as bibliotecas cuda, no debian buster

```
sudo apt install libcuda libcudart libcublas libcublasLt libcufft libcurand libcusolver libcusparse
```

A biblioteca `libcudnn` deve ser manualmente baixada no site da nvidia

https://developer.nvidia.com/rdp/cudnn-download

Baixar a versão correta para o cuda instalado no computador no caso do debian
buster CUDA 11.1, os pacotes .deb do ubuntu 20 funcionam.


E configurar :

```
export XLA_FLAGS="--xla_gpu_cuda_data_dir=/usr/lib/cuda"
export TF_XLA_FLAGS="--tf_xla_enable_xla_devices"
```

Um warning é dado por um erro no ID numa da placa de video, para resolver isso
o seguinte codigo deve ser executado a cada boot

```
echo 0 | sudo tee -a /sys/bus/pci/devices/0000\:01\:00.0/numa_node
```

Não ha problema em nao executar este comando, visto que é somente um warning e
a biblioteca consegue identificar a placa de video corretamente.

O ID PCI da placa no comando acima é um exemplo, mas normalmente este é o ID da
primeira placa de video encontrada.


## Estrutura do projeto

### aux

Diretorio contendo dados auxiliares extraidos e processados dos dados originais
da aquisicao.

#### rock_ids_agp.txt

Arquivo contendo o codigo de rocha e o nome da rocha baseado nos dados dos
arquivos AGP. 

Formato:

NN XXXXXXX

Onde:

 - NN: e' o codigo da rocha em dois caracteres alinhado a direita sem zeros
 - XXXXXXX: e' a identificacao da rocha sem limite de caracteres, iniciando na
            coluna 4


### inputs

Diretorio contendo os dados de entrada de pocos para processamento, dentro
deste diretorio os dados sao segmentados em subdiretorios por identificador de
poco.


### outputs

Saida dos programas. E' importante que os testes tenham no nome do arquivo um
timestamp  YYYYMMDDHHMMSS . E as iniciais Exemplo:

`20201201191523_I_NOMEDOARQUIVO.ttt`

### logs

Diretorio contendo os arquivos com os parametros de cada execucao de testes que
devem ser passiveis de reproducao. Respeitar a nomeclatura utilizada em
`outputs`


### Refs

Diretorio contendo artigos e referencias utilizado no projeto.

#### Papers

Artigos referencia

#### notes

Notas pessoais do projeto

### nb

Diretorio contendo jupyter notebooks de prototipagem.

### tex

Diretorio contendo documentos/artigos de resumos expandidos para serem submetidos aos
congressos. Este diretorio deve ser subdividido por submissao.


## Algoritmo de Kohonen

Dado um espaço de N caracteristicas a serem modeladas. Criamos um tensor
arbitrário de dimensões $M x N x O$, chamado $W$, onde $M x N$ é a dimensão
cada camada do modelo Kohonen indexada por $i, j$.

Cada camada definida por um plano $M x N$ presenta um atributo, assim se houver
5 atribuitos ($O = 5$) teremos então um tensor de dimensões $M x N x 5$. 

Por definição chamamos todos os $O$ valores da $i,j$-ésima posição do mapa
como uma linha neuronal.

TODO: Tamanho otimo do plano $N x M$.

### Treinamento

1. Preenchemos o mapa $W$ com valores aleatórios próximos de zero (TODO:
   procurar uma boa distribuição que satisfaça este critério). Outra
   possibilidade de abordagem para o preenchimento dos dados iniciais é
   utilizar uma distribuição uniforme baseados nos valores mínimos e máximos
   esperados de cada camada (por exemplo se a camada 2, relacionada com o
   atribuito profundidade varia de 100 a 2000, colocamos dados distribuidos
   neste intervalo.). TODO: Analisar se a distribuição uniforme é uma
   alternativa melhor do que o método de números próximos de 0 ou tentar
   identificar por inferencia estatística qual a distribuição esperada em cada
   tipo de dado.

2.  Criar um tensor vazio de $N x M$ chamado `CLASS`.

3. Para cada entrada $r$ no CONJUNTO DE TREINAMENTO, onde cada entrada é $O$
   dimensional. Fazer:

3.1 Para cada $W_ij$ em $W$.

3.1.1 $delta_ij = | r - W_ij |_2^2$_

3.2 Encontrar o  $ij$-ésima linha neuronal com a menor distância l2.
Chamaremos esta linha de $N\*$, ou a "linha neuronal vencedora".

3.3 Preencher a $ij$-ésima posição do tensor `CLASS` com a mesma `class_id` da
entrada vencedora.

3.4.  Para cada VIZINHO do conjunto $ADJ(aN\*)$.

3.4.1 Aplicar o procedimento $APRENDIZAGEM$ em $VIZINHOS$


#### Definição de vizinhos

No modelo, VIZINHOS são o conjunto dos elementos adjacentes mais próximos de
cada uma das bordas do elemento $N\*$. Utilizando as coordenadas espaciais de
uma malha retangular eles são dados pelos conjuntos dados por

$$
ADJ(N\*) = {
            (N*_i + 1 % M, N*_j        ),
            (N*_i - 1 % M, N*_j        ), 
            (N*_i        , N*_j + 1 % N), 
            (N*_i        , N*_j - 1 % N), 
	  }
$$


#### Sobre aprendizagem:

Função ETA de resfriamento é dada por

Nu^n = Nu^0 ( 1 - (t / T)) 

onde: t = numero da iteração, T é o numero total de épocas e Nu é o fator de
aprendizagem onde Nu^0 é o fator inicial arbitrario.

### Fitting

FALTA ESCREVER!!!
 
## Descricao dos codigos

### Perftests

Conjunto de tests para verificar a performance do codigo e as melhores
abordagens para a computação do modelo de kohonen. Testes feito com python e
Fortran, código em python utilizando SCIPY e cKDtree teve um speedup de 22x
comparado ao algoritmo em Fortran.

#### fdist.f95

Algoritmo do modelo de Kohonen feito em fortran. Somente a etapa de calculo de
neuronio vencedor. Sem a classificao.

Para rodar:

```
make
./fdist
```



#### pdist.py

Algoritmo do modelo de Kohonen feito em python. Diversas abordagns foram
analisadas:

1. Matriz de diferencas feita em numpy.array, norma calculada elemento a
   elemento.

2. Matriz de diferencas feita em numpy.array, norma calculada com operadores
   vetorizados do numpy.

3. Operação feita inplace utilizando vetorizacao numpy.

4. MAtriz de diferenças em numpy, operaração feita utilizando iteração sobre as
   linhas.

5. Matriz de diferenças em numpy, norma calculada utilizando
   numpy.euclidean_distances.

6. Matriz numpy, operações executadas com Numba JIT.

7. Matriz numpya com distancia calculada utilizando scipy.cdist.

8. Matriz numpy convertida em pontos de dados, distancias calculadas
   utilizando cKDTrees.

9. Matriz de diferencas utilizando tensores. Operações calculadas utilizando
   tensorflow.

10. Matriz de difenrencas utilizando tensores.

Deve ser executado dentro do ipython e cada teste de performance deve ser
chamado individualmente.

Exemplo

```
ipython3 -i pdist.py
```

Dentro do ipython executar

```
%timeit method5(R, W)
```

#### src/kohonen.f95

Algoritmo kohonen. 

```
make
./kohonen
```

#### acoplador.py

Adicona o programa que faz a filtragem de dados expúrios ferramentais,
desmoronamentos e acopla o arquivo agp com o arquivo `*.las`. Gera imagem de
análise e salva o dataframe.


#### srctmp/perftests/randomaccess.py

Teste de performance em diferentes tipos de datasets para velocidade e leitura
e escrita de grandes volumes de dados serao testados oa datasets: NumpyArray,
Zarray, pandas dataframe, xarray, python lists e tensorflow array. Ainda sem
conclusões.

Atualmente o programa gera somente uma saida em texto para ser executada dentro
do `ipython`. 

### readagp.py

### readdLis.py

Teste de leitura de um arquivo do tipo DLIS usando a biblioteca dlisio.

### readlis.py

Leitura de arquivo LIS utilizando a biblioteca TotalDepth, o codigo atual
comentado permite: 1. listagem dos atribuitos, 2. Interpolacao de dados
faltantes, 3. Geracao de grafico de poco com atribuitos selecionados.

*Este é a abordagem recomendada para o problema.*


### extract_rock_ids.sh

Extrai os ROCK IDs de um arquivo de catalogo

Uso:

```
cat [ARQUIVOSAGP...] | ./extract_rock_ids.sh
```

### rock_ids_agp.txt

Arquivo de saida do script `extract_rock_ids.sh` que permite a indexação de
todas litografias encontradas.

## Convertendo LISt (LIS com TIF) em LIS

Com o totaldepth instalado execute:

```
tddetif DIRETORIOENTRADA DIRETORIOSAIDA
```

Os arquivos LISt terao suas tags tif removidas e uma copia sera colocada no
arquivo de saida.

Apos isso renomear os arquivos dentro do `DIRETORIOSAIDA` com a extensao
`.lis`.


## Guia merge

1. Para criar um branch

```
git branch NOMEDOBRANCH
```

2. Mude para o seu branch

```
git checkout NOMEDOBRANCH
```

3. Faca todas suas edicoes... quando finalizar adicione duas mudancas

```
git add ARQUIVOSALTERADOS
git commit -m 'MENSAGEM CURTA DE COMMIT NAO MAIS QUE 100 CARACTERES'
```

4. Submeta o seu branch

```
git push
```

Voce pode executar os pacoes anteriores (3, 4) tantas vezes forem necessarias
ateh que tenha atingido o seu objetivo.

5. Finalizado integre seu branch ao master

```
git checkout master
git merge NOMEDOBRANCH
```

6. Se tudo deu certo, sua mudanca foi aplicada, fique a vontade para remover o
   seu branch finalizado

```
git branch -d NOMEDOBRANCH
git commit -m 'NOMEDOBRANCH removido'
git push
```

7. BE HAPPY!


## Ideias

Visualização da esparsidade dos dados do poco.

datanans = df[df.isna()].to_numpy()
columns = df.columns()

fig, ax = plt.subplots(1, 1, figsize=(5,5), dpi=150)
ax.eye(datanans, scale='auto')
