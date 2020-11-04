# Kohonen

Este repositório é o conjunto de esforços para o uso do modelo de Kohonen de
classificação de uma rede neuronal aplicada a identificação de litografias.

O objetivo deste trabalho é a identificação do melhor conjunto de atributos
para a classificação. Inicialmente o método aplicado será o uso de algoritmos
genéticos multi objetivos utilizando o modelo de Kohonen como função
custo.

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

TODO: ESCREVER


# Plano de trabalho: reunião de 14 de fevereiro de 2020

* Conseguir ler os dados LIS e DLIS ** FEITO
* Filtragem dos dados para criar o dataset de entrada. Descobrir quais dados possuem todos os atributos
* Escrever o kohonen baseado no kohonen.py e no kohonen.for no tensor flow ** PARCIAL
* Validar o código no tensor flow com o fortran usando o mesmo dataset.
* Criar o programa de algoritmo genético multi-objetivo com o tensor flow utilizando o kohonen como critério de convergência
* Gerar resultados. Pensar em como rodar o dado em múltiplas instituições. 
* Escrever o artigo

*Total*: 192 dias 

## TO DO (meeting de 18 de outubro de 2020)
 * Fazer o compartilhamento dos arquivos agp e DLIS via gdrive (Victor)
 * Seleção e upload dos dados compartilhados para a pasta inputs (Igor)
 * Fazer o upload para a pasta programs/src (nome mais comum) do programa de filtragem e acoplamento (Victor)
 * Fazer o upload dos programas que foram usados para testes decritos neste README (igor)
 
 
## Descricao dos codigos

### Perftests

Conjunto de tests para verificar a performance do codigo e as melhores
abordagens para a computação do modelo de kohonen. Testes feito com python e
Fortran, código em python utilizando SCIPY e cKDtree teve um speedup de 22x
comparado ao algoritmo em Fortran.

#### fdist.f95

Algoritmo do modelo de Kohonen feito em fortran

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


#### acoplador.py

Adicona o programa que faz a filtragem de dados expúrios ferramentais,
desmoronamentos e acopla o arquivo agp com o arquivo `*.las`. Gera imagem de
análise e salva o dataframe.


#### randomaccess.py

Teste de performance em diferentes tipos de datasets para velocidade e leitura
e escrita de grandes volumes de dados serao testados oa datasets: NumpyArray,
Zarray, pandas dataframe, xarray, python lists e tensorflow array. Ainda sem
conclusões.

TODO: Verificar os tipos de dados (volume e dimensões) para poder executar o
benchmark correto e encontrar o formato que melhor atende as demandas
computacionais.

### readagp.py

### readdLis.py

Teste de leitura de um arquivo do tipo DLIS usando a biblioteca dlisio.

### readlis.py

Leitura de arquivo LIS utilizando a biblioteca TotalDepth, o codigo atual
comentado permite: 1. listagem dos atribuitos, 2. Interpolacao de dados
faltantes, 3. Geracao de grafico de poco com atribuitos selecionados.

*Este é a abordagem recomendada para o problema.*

### rock_ids_agp.txt

Arquivo de saida do script `extract_rock_ids.sh` que permite a indexação de
todas litografias encontradas.

### extract_rock_ids.sh

Extrai os ROCK IDs de um arquivo de catalogo
