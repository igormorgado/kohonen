#!/usr/bin/env python

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys

# Constantes de analise de qualidade do dado

def fields_filter(df, filterlist=['DEPT', 'RIDS', 'LITO']):
    return [field for field in df.columns if field not in filterlist]

def total_column_fullness(df):
    fields = fields_filter(df)
    return df[fields].notna().sum()/df[fields].shape[0]

def total_data_fullness(df):
    fields = fields_filter(df)
    return  total_column_fullness(df[fields]).mean()

def first_full_frame(df):
    fields = fields_filter(df)
    return  df[fields][ df.notna().all(axis=1) == True ].iloc[0]

def first_full_frame_idx(df):
    fields = fields_filter(df)
    return first_full_frame(df[fields]).name

def internal_column_fullness(df):
    fields = fields_filter(df)
    idx = first_full_frame_idx(df[fields])
    return df[fields][idx:].notna().sum()/df[fields][idx:].shape[0]

def internal_data_fullness(df):
    fields = fields_filter(df)
    return internal_column_fullness(df[fields]).mean()

def fullness_column_ratio(df):
    fields = fields_filter(df)
    return total_column_fullness(df[fields]) / internal_column_fullness(df[fields])

def fullness_ratio(df):
    fields = fields_filter(df)
    return total_data_fullness(df[fields]) / internal_data_fullness(df[fields])


def fullness_matrix_plot(fmatrix):

    # Sort matrix by column usage.
    columns_usage = fmatrix.notna().sum()
    columns_sorted = columns_usage.sort_values(ascending=False)
    fmatrix_sorted = fmatrix[columns_sorted.index]

    with open("outputs/attribute_presence.txt", "w") as fd:
        for k, v in columns_sorted.iteritems():
            fd.write(f"{k:4s}: {v:3d}\n")
    fd.close()

    plt.figure(figsize=(21,7), dpi=150)
    plt.pcolor(fmatrix, shading='flat', edgecolors='black', cmap='cividis')
    plt.yticks(np.arange(0.5, len(fmatrix_sorted.index), 1), fmatrix_sorted.index, fontsize=4)
    plt.xticks(np.arange(0.5, len(fmatrix_sorted.columns), 1), fmatrix_sorted.columns, fontsize=4, rotation=90)
    plt.colorbar(label='Fullness',pad=0.01)
    plt.title("Fullness matrix")
    plt.xlabel("Attributes")
    plt.ylabel("Well name")
    plt.tight_layout()
    plt.savefig('outputs/fullness_matrix.png', dpi=300, bbox_inches='tight')


def main():
    # User filenames from command arguments?
    if len(sys.argv) < 2:
        print("Usage: {sys.argv[0]} [pandas_well_files] ...")
        sys.exit()

    files = sys.argv[1:]

    # Compute fullness matrix for files in files
    fullness_matrix = pd.DataFrame()
    for f in files:
        df = pd.read_pickle(f)
        well = os.path.splitext(os.path.basename(f))[0]
        wellname = well[:len(well)//2]
        fcr = fullness_column_ratio(df)
        fcr.name = wellname
        fullness_matrix = fullness_matrix.append(fcr)

    fullness_matrix.sort_index(inplace=True)

    # Plot the fullness matrix
    fullness_matrix_plot(fullness_matrix)

if __name__ == "__main__":
    main()

