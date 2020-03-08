Parametros para teste:

Tamanho do Tabuleiro: 40 x 40
Atributos: 4

Dados de Entrada: 697
Epocas: 1000

RESULTADOS:

Fortran:
       17.6 ms
Python:   
	1.6 ms(numba)
        3.6 ms(scipy/cdist)
        5.8 ms(sklearn/euclidean_distances)
       31.2 ms(numpy/naive)
