import pandas as pd
import numpy as np
import TotalDepth
from TotalDepth.LIS.core import File
from TotalDepth.LIS.core import FileIndexer
from TotalDepth.LIS.core import LogiRec
from TotalDepth.LIS.core import LogPass


files = pd.read_csv("inputs/proc/def.txt", comment="#")

for filename in files["LIS"]:
    print("")
    print("")
    filename = f"inputs/{filename}"
    filehandler = File.FileRead(filename)
    fileindex = FileIndexer.FileIndex(filehandler)
    log_passes = fileindex.genLogPasses()
    log_records = fileindex.genAll()
    log_passes_list = list(log_passes)
    log_records_list = list(log_records)
    for idx, x in enumerate(log_passes_list):
        x.logPass.setFrameSet(filehandler, None, None)
        channel_scheme = list(x.logPass.genFrameSetScNameUnit())
        fields, units = list(zip(*channel_scheme))
        fields = [f.strip() for f in fields]
        if 'DUMM' in fields:
            continue
        data = x.logPass.frameSet.frames
        if (data.shape[1] != len(fields)):
            #print(f"{filename} {idx} DIFF: shape {data.shape[1]} cols {len(fields)}", flush=True)
            print(f"{filename} {idx:3d} ER: {len(fields):4d} {fields}", flush=True)
        else:
            print(f"{filename} {idx:3d} OK: {len(fields):4d} {fields}", flush=True)

#
#    #print(x.tocStr())
#
##
#lp = log_passes_list[0]
#
## Load the data headers
#lp.logPass.setFrameSet(filehandler, None, None)
#idx=0
#
## Clean up fields and units names.
#channel_scheme = list(lp.logPass.genFrameSetScNameUnit())
#fields, units = list(zip(*channel_scheme))
#fields = [f.strip() for f in fields]
#units = [u.strip() for u in units]
#
## Adding indexes in fields to keep track of passes
#nf = []
#for val in fields:
#    if val != 'DEPT':
#        val = f'{val}_{idx}'
#    nf.append(val)
#fields = nf
#
## Build dataframe from data
#data = lp.logPass.frameSet.frames
#if (data.shape[1] != len(fields)):
#    print(f"{filename} DIFF({idx}): shape {data.shape[1]} cols {len(fields)}")
#
## Copy data as pandas dataframe
#df = pd.DataFrame(data, columns=fields)
#
##
## FILTERS
##
#
## Spurious values
#df.replace(-999.25, np.nan, inplace=True)
#df.replace(-9999.25, np.nan, inplace=True)
#df.replace(-999999.9999, np.nan, inplace=True)
#
## Find duplicate fields and merge them by average
#if merge_fields:
#    seen = {}
#    dupes = []
#
#    for field in fields:
#        if field not in seen:
#            seen[field] = 1
#        else:
#            if seen[field] == 1:
#                dupes.append(field)
#            seen[field] += 1
#
#    for field in dupes:
#        field_tmp = f'{field}_TMP'
#        df[field_tmp] = df[field].mean(axis=1)
#        df.drop(field, axis=1, inplace=True)
#        df.rename(columns={field_tmp: field}, inplace=True)
#
## Convert dept from ft to mts
#if units[0] == 'FT':
#    df['DEPT'] = df['DEPT'] * 0.3048
#
#
## Merge dataframe
##dff = pd.merge(dff, df, how='outer', on='DEPT')
#
## Sort by DEPT and reindexes
##dff.sort_values('DEPT', inplace=True, ignore_index=True)
