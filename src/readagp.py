#!/usr/bin/env python
import numpy as np
from itertools import chain
import os
import sys

rockids = {2: 'CALCARIO CRISTAL',
           6: 'CALCILUTITO',
           7: 'CALCISSILTITO',
           8: 'CALCARENITO',
           10: 'CALCIRUDITO',
           30: 'DOLOMITO',
           40: 'BRECHA',
           42: 'CONGLOMERADO',
           44: 'DIAMICTITO',
           46: 'TILITO',
           48: 'AREIA',
           49: 'ARENITO',
           54: 'SILTITO',
           55: 'ARGILA',
           56: 'ARGILITO', 
           57: 'FOLHELHO',
           58: 'MARGA',
           64: 'IGNEA NAO IDENT.',
           65: 'DIABASIO',
           66: 'BASALTO',
           67: 'GRANITO',
           70: 'METAMOR.NAO IDE.',
           71: 'GNAISSE',
           73: 'XISTO',
           74: 'QUARTZITO',
           75: 'META-ARENITO',
           76: 'META-SILTITO',
           82: 'ANIDRITA',
           83: 'GPSITA',
           92: 'CARVAO',
           94: 'SILEX'}


def read_agp(fpath):
    # TOPO BASE ROCHA CARACTERISTICAS
    lito_data = []
    foundlito = False
    lines_to_skip = 2
    with open(fpath, 'r', encoding='iso-8859-1') as fd:
        for line in fd:
            # Encontrou a sessao de Litologia
            if 'LITOLOGIA -' in line:
                foundlito = True
                continue

            # Fim da sessao de Litologia
            if 'RESUMO DAS ROCHAS ENCONTRADAS NO POCO' in line:
                break

            # Dentro da sessao de Litologia
            if foundlito:
                # Primeira linha e' especial
                if lines_to_skip == 0:
                    rline = line.strip().replace('(','').replace(')','').split()
                    topo = rline[:2]
                    base = rline[2:4]
                    rocha = [rline[4]]
                    lito_data.append(list(chain(topo, base, rocha)))

                # Outras linhas
                if lines_to_skip < 0:
                    rline = line.strip().replace('(','').replace(')','').split()
                    topo = base
                    base = rline[:2]
                    rocha = [rline[2]]
                    lito_data.append(list(chain(topo, base, rocha)))

                lines_to_skip -= 1

    lito_data = np.array(lito_data, dtype=float)

    return lito_data


def find_rock(data, depth, sealevel=False):
    if not sealevel:
        rockid = data[(data[:,0] <= depth) & (depth <= data[:,2])][:,4]
    else:
        rockid = data[(data[:,1] <= depth) & (depth <= data[:,3])][:,4]

    if len(rockid) == 0:
        rockid = None
    else:
        rockid = int(rockid.flatten()[0])

    return rockid


def main(args):
    fpath = sys.argv[1]
    depth = int(sys.argv[2])
    litodata = read_agp(fpath)

    if len(litodata) == 0:
        print(f'{sys.argv[0]}: No litology found at {fpath}', file=sys.stderr)
        sys.exit(1)

    try:
        rock = rockids[find_rock(litodata, depth)]
    except KeyError as e:
        print(f'{sys.argv[0]}: No rock found at {depth}', file=sys.stderr)
        sys.exit(2)
    else:
        print(rock)

    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <AGP_FILENAME> <DEPTH>', file=sys.stderr)
        sys.exit(0)

    main(sys.argv[0])


