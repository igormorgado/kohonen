#!/usr/bin/env python3

import sys
import os
from itertools import chain
import pandas as pd
import numpy as np

import TotalDepth
from TotalDepth.LIS.core import File
from TotalDepth.LIS.core import FileIndexer
from TotalDepth.LIS.core import LogiRec

import matplotlib.pyplot as plt

def lis_to_dataframe(filename, merge_fields=True):
    """Read a LIS file and return a formatted pandas dataframe"""

    if not os.path.isfile(filename):
        return None

    filehandler = File.FileRead(filename)
    fileindex = FileIndexer.FileIndex(filehandler)

    log_passes = fileindex.genLogPasses()
    log_records = fileindex.genAll()

    log_passes_list = list(log_passes)
    log_records_list = list(log_records)

    # Load framesets
    logpass_units = []
    dff = pd.DataFrame(columns=['DEPT'])
    
    idx = 0
    for lp in log_passes_list:

        # Load the data
        lp.logPass.setFrameSet(filehandler)

        channel_scheme = list(lp.logPass.genFrameSetScNameUnit())
        fields, units = list(zip(*channel_scheme))
        fields = [f.strip() for f in fields]
        units = [u.strip() for u in units]

        # Skip dummy framesets
        if 'DUMM' in fields:
            continue

        # Adding indexes in fields to keep track of passes
        nf = []
        for val in fields:
            if val != 'DEPT':
                val = f'{val}_{idx}'
            nf.append(val)
        fields = nf

        # Build dataframe from data
        data = lp.logPass.frameSet.frames
        df = pd.DataFrame(data, columns=fields)

        #
        # FILTERS
        #

        # Spurious values
        df.replace(-999.25, np.nan, inplace=True)
        df.replace(-999999.9999, np.nan, inplace=True)

        # Find duplicate fields and merge them by average
        if merge_fields:
            seen = {}
            dupes = []

            for field in fields:
                if field not in seen:
                    seen[field] = 1
                else:
                    if seen[field] == 1:
                        dupes.append(field)
                    seen[field] += 1

            for field in dupes:
                field_tmp = f'{field}_TMP'
                df[field_tmp] = df[field].mean(axis=1)
                df.drop(field, axis=1, inplace=True)
                df.rename(columns={field_tmp: field}, inplace=True)

        # Convert dept from ft to mts

        if units[0] == 'FT':
            df['DEPT'] = df['DEPT'] * 0.3048
        #    print(f"Recall {idx} in feet")
        # else:
        #     print(f"Recall {idx} in meters")

        #print(units)

        # FILTERS MUST BE APPLIED BEFORE IDX NAMING
        # # ILD < 600
        # if 'ILD' in fields:
        #     df['ILD'] = np.where(df['ILD'].gt(600), np.nan, df['ILD'])

        # # SFLU < 1000
        # if 'SFLU' in fields:
        #     df['SFLU'] = np.where(df['SFLU'].gt(1000), np.nan, df['SFLU'])

        # # CILD < 1000
        # if 'CILD' in fields:
        #     df['CILD'] = np.where(df['CILD'].gt(1000), np.nan, df['CILD'])

        # Merge dataframe
        dff = pd.merge(dff, df, how='outer', on='DEPT')

        # Next iteration
        idx += 1

    # Sort by DEPT and reindexes
    dff.sort_values('DEPT', inplace=True, ignore_index=True)

    return dff


def lito_ids(fpath):
    """Read litology IDS from a CSV file"""
    lito_ids_df = pd.read_csv(fpath, names=['id', 'lito'])
    return lito_ids_df


def lito_from_agp(fpath):
    """Read litology from AGP file"""

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


def find_rock_id(data, depth, sealevel=False):
    """Return a rock id, given a AGP litography data and a depth level"""
    if not sealevel:
        rockid = data[(data[:,0] <= depth) & (depth <= data[:,2])][:,4]
    else:
        rockid = data[(data[:,1] <= depth) & (depth <= data[:,3])][:,4]

    if len(rockid) == 0:
        rockid = None
    else:
        rockid = int(rockid.flatten()[0])

    return rockid



#############################################################################
### MAIN
#############################################################################


# root_dir  = '/home/igor/Projects/kohonen/inputs/'
# proc_file = '/home/igor/Projects/kohonen/inputs/proc/novo.txt' 

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} PROCFILE ROOTDIR")
    sys.exit()

root_dir = sys.argv[2]
proc_file = sys.argv[1]


proc_df = pd.read_csv(proc_file, comment='#')

lis = []
lit = []
agp = []
names = []


for idx, row in proc_df.iterrows():

    # Check if configured files exist
    lis_filepath = os.path.join(root_dir, row['LIS'])
    if not os.path.isfile(lis_filepath):
        print(f"Filepath {lis_filepath} not found. ERROR.")
        sys.exit(1)

    name = os.path.splitext(os.path.basename(lis_filepath))[0]
    names.append(name)
    print(f"Loading {name}")

    agp_filepath = os.path.join(root_dir, row['AGP'])
    if not os.path.isfile(agp_filepath):
        print(f"Filepath {agp_filepath} not found. ERROR.")
        sys.exit(1)

    lit_filepath = os.path.join(root_dir, row['LITO'])
    if not os.path.isfile(lit_filepath):
        print(f"Filepath {lit_filepath} not found. ERROR.")
        sys.exit(1)

    nlis = lis_to_dataframe(lis_filepath)
    nagp = lito_from_agp(agp_filepath)
    nlit = lito_ids(lit_filepath)

    rids = []
    rnms = []
    for idx, row in nlis.iterrows():
        rock_id = find_rock_id(nagp, row['DEPT'])
        if rock_id is None:
            rock_name = None
        else:
            rock_name = nlit[nlit['id'] == rock_id]['lito'].iloc[0]

        rids.append(rock_id)
        rnms.append(rock_name)

    nlis['RIDS'] = rids
    nlis['LITO'] = rnms

    lis.append(nlis)


# Encontra prefixos para filtrar
prefixes = []
for well in lis:
    prefixes.extend(list(set([ x.split('_')[0] for x in sorted(list(well.columns))])))

# Estes campos não devem ser filtrados
prefixes.remove('LITO')
prefixes.remove('RIDS')
prefixes.remove('DEPT')

# Para cada lis
for name, data in zip(names,lis):
    l = data.copy()

    print(f"Filtering {name}")
    # Drop Lito inexistente
    l = l[l['LITO'].notna()]

    # Interpola entre multiplas RUNS
    for pref in prefixes:
        print(f"{pref} ", end="", flush=True)
        regex_str = f'{pref}_[0-9]+'
        l[pref] = l.filter(regex=regex_str).mean(axis=1)
        drop_columns = l.filter(regex=regex_str).columns
        l.drop(columns=drop_columns, inplace=True)
    print()

    # Remove colunas que são somente NaNs 
    l.dropna(axis=1, how='all', inplace=True)

    # Interpola em profundidade
    l.set_index('DEPT', inplace=True)
    l.interpolate(method='values', inplace=True)
    l.reset_index(inplace=True)

    # Remove todas as linhas que são somente NAN
    l.dropna(axis=0, how='all', inplace=True)

    filename = os.path.join(root_dir, "merged", name)
    print(f"Saving {filename}")
    l.to_pickle(f"{filename}.pd")
    l.to_csv(f"{filename}.csv", sep=' ', index=False, float_format='%.8f')
    print()
