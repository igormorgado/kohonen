import TotalDepth
from TotalDepth.LIS.core import File
from TotalDepth.LIS.core import FileIndexer

import os


dirname = 'data/input/lis'
basename = '1API_0001__PR_1API_0001__PR.lis'

filepath = os.path.join(dirname, basename)

try:
    print(f'Reading index from {basename}')
    lis_file = File.FileRead(filepath)
    lis_idx = FileIndexer.FileIndex(lis_file)
except RuntimeError as e:
    print(f'Error loading {filepath}')

# log_passes = list(lis_idx.genLogPasses())
# lp = log_passes[0].logPass
# lpdict = lp.jsonObject()
# 
# numchannels = lpdict['Plan']['NumChannels']
# channels = lpdict['Channels']
# firstval = lpdict['Xaxis']['FirstValOptical']
# lastval = lpdict['Xaxis']['LastValOptical']
# totalframes = lpdict['Xaxis']['TotalFrames']
# spacing = lpdict['Xaxis']['SpacingOptical']
# units = lpdict['Xaxis']['UnitsOptical']
# nullvalue = lp.nullValue
# 
# 
# #print(f'nullValue           {lp.nullValue}')
# print(f'numchannels         {numchannels}')
# print(f'channels            {channels}')
# print(f'firstval            {firstval}')
# print(f'lastval             {lastval}')
# print(f'totalframes         {totalframes}')
# print(f'spacing             {spacing}')
# print(f'units               {units}')

# lp.setFrameSet(lis_file)
# data = lp.frameSet.frames
# 
# data[data == nullvalue] = np.nan
# 
# depth = data[:,0]
# c1 = data[:,9]
# c2 = data[:,10]
# 
# import scipy as sp
# import numpy as np

# new_x_c1 = np.linspace(0, len(c1), 5000)
# new_x_c2 = np.linspace(0, len(c2), 5000)
# new_c1 = sp.interpolate.interp1d(np.arange(len(c1)), c1, kind='cubic')(new_x_c1)
# new_c2 = sp.interpolate.interp1d(np.arange(len(c2)), c2, kind='cubic')(new_x_c2)

#import matplotlib.pyplot as plt
#
#fig, ax1 = plt.subplots(1, 1, figsize=(15,3), dpi=150)
#
#ax1.plot(c1, 'ro-', markersize=.5, alpha=.5, label='C1')
#ax1.plot(c2, 'bo-', markersize=.5, alpha=.5, label='C2')
#
#ax2 = ax1.twinx()
#ax2.plot(depth, 'k', label='Depth')
#
#ax1.set_xlabel = 'Datapoint'
#fig.legend(loc='upper right')
#plt.tight_layout()
#plt.show()


# lis_all = list(lis_idx.genAll())
# count = 0
# mcount = 0
# 
# # Print the headers
# for idx, x in enumerate(lis_all):
#     if isinstance(x, TotalDepth.LIS.core.FileIndexer.IndexTable):
#         print(mcount, count, x.name)
#         count += 1
#     if isinstance(x, TotalDepth.LIS.core.FileIndexer.IndexFileTail):
#         mcount += 1
#         count = 0
#         print()


# reelhead = lis_all[0]
# tapehead = lis_all[1]
# filehead = lis_all[2]
# fileidx0 = lis_all[3]
# fileidx1 = lis_all[4]
# fileidx2 = lis_all[5]
# fileidx3 = lis_all[6]
# fileidx4 = lis_all[7]
# unknown = lis_all[22]
# logpass = lis_all[23]
# filetail = lis_all[24]

#print(reelhead)
#print(tapehead)
#print(filehead)
#print(fileidx0)
#print(fileidx1)
#print(unknown)
#print(logpass)
#print(filetail)

# logicalRecordTypes:
# 132 TotalDepth.LIS.core.FileIndexer.IndexReelHead
# 130 TotalDepth.LIS.core.FileIndexer.IndexTapeHead
# 128 TotalDepth.LIS.core.FileIndexer.IndexFileHead
#  34 TotalDepth.LIS.core.FileIndexer.IndexTable
# 232 TotalDepth.LIS.core.FileIndexer.IndexUnknownInternalFormat
#  64 TotalDepth.LIS.core.FileIndexer.IndexLogPass
# 129 TotalDepth.LIS.core.FileIndexer.IndexFileTail

#print('Play with:  reelhead tapehead filehead fileidx0 ... 4')
# reelhead.logicalRecord.date
#print('REELHEAD')
#print(f'attr           {reelhead.logicalRecord.attr}')
#print(f'date           {reelhead.logicalRecord.date}')
#print(f'name           {reelhead.logicalRecord.name}')
#print(f'ymd            {reelhead.logicalRecord.ymd}')
#print(f'comments       {reelhead.logicalRecord.comments}')
#print(f'desc           {reelhead.logicalRecord.desc}')
#print(f'origin         {reelhead.logicalRecord.origin}')
#print(f'serviceName    {reelhead.logicalRecord.serviceName}')
#print(f'contNumber     {reelhead.logicalRecord.contNumber}')
#print(f'prevReelName   {reelhead.logicalRecord.prevReelName }')
#print()


#print('TAPEHEAD')
#print(f'attr           {tapehead.logicalRecord.attr}')
#print(f'date           {tapehead.logicalRecord.date}')
#print(f'name           {tapehead.logicalRecord.name}')
#print(f'ymd            {tapehead.logicalRecord.ymd}')
#print(f'comments       {tapehead.logicalRecord.comments}')
#print(f'desc           {tapehead.logicalRecord.desc}')
#print(f'origin         {tapehead.logicalRecord.origin}')
#print(f'serviceName    {tapehead.logicalRecord.serviceName}')
#print(f'contNumber     {tapehead.logicalRecord.contNumber}')
#print()

#print('FILEHEAD')
#print(f'attr           {filehead.logicalRecord.attr}')
#print(f'desc           {filehead.logicalRecord.desc}')
#print(f'version        {filehead.logicalRecord.version}')
#print(f'contFileName   {filehead.logicalRecord.contFileName}')
#print(f'FileName       {filehead.logicalRecord.fileName}')
#print(f'FileType       {filehead.logicalRecord.fileType}')
#print(f'maxPrLength    {filehead.logicalRecord.maxPrLength}')
#print(f'serviceSubLvl  {filehead.logicalRecord.serviceSubLevel}')
#print(f'date           {filehead.logicalRecord.date}')
#print(f'ymd            {filehead.logicalRecord.ymd}')
# print(f'prevFileName   {filehead.logicalRecord.prevFileName}')
# print()
# 
# print('FILETAIL')
# print(f'attr           {filetail.logicalRecord.attr}')
# print(f'desc           {filetail.logicalRecord.desc}')
# print(f'version        {filetail.logicalRecord.version}')
# print(f'contFileName   {filetail.logicalRecord.contFileName}')
# print(f'FileName       {filetail.logicalRecord.fileName}')
# print(f'FileType       {filetail.logicalRecord.fileType}')
# print(f'maxPrLength    {filetail.logicalRecord.maxPrLength}')
# print(f'serviceSubLvl  {filetail.logicalRecord.serviceSubLevel}')
# print(f'date           {filetail.logicalRecord.date}')
# print(f'ymd            {filetail.logicalRecord.ymd}')
# print(f'nextFileName   {filetail.logicalRecord.nextFileName}')
# print()

# print('LogPass')
# logpass = log_passes[0]

# print(f'frameSet                {logpass.logPass.frameSet}')
# print(f'iflrType                {logpass.logPass.iflrType}')
# print(f'xAxisIndex              {logpass.logPass.xAxisIndex}')
# print(f'isIndirectX             {logpass.logPass.isIndirectX}')
# print(f'numBytes                {logpass.logPass.numBytes}')
# print(f'nullValue               {logpass.logPass.nullValue}')
# print(f'xAxisFirstEngVal        {logpass.logPass.xAxisFirstEngVal}')
#logpass.logPass.xAxisFirstEngVal.value
#logpass.logPass.xAxisFirstEngVal.uom
# print(f'xAxisLastEngVal         {logpass.logPass.xAxisLastEngVal}')
#logpass.logPass.xAxisLastEngVal.value
#logpass.logPass.xAxisLastEngVal.uom

# print(f'xAxisFirstValOptical    {logpass.logPass.xAxisFirstValOptical}')
# print(f'xAxisLastValOptical     {logpass.logPass.xAxisLastValOptical}')
# print(f'xAxisSpacingOptical     {logpass.logPass.xAxisSpacingOptical}')
# print(f'xAxisUnitsOptical       {logpass.logPass.xAxisUnitsOptical}')


# print(f'xAxisFirstVal           {logpass.logPass.xAxisFirstVal}')
# print(f'xAxisLastVal            {logpass.logPass.xAxisLastVal}')
# print(f'xAxisSpacing            {logpass.logPass.xAxisSpacing}')
# print(f'xAxisUnits              {logpass.logPass.xAxisUnits}')
# print(f'totalFrames             {logpass.logPass.totalFrames}')
# Expected Total Frames
#totalFrames = 1 + (logpass.logPass.xAxisLastVal - logpass.logPass.xAxisFirstVal ) / logpass.logPass.xAxisSpacing ) 


#lp = logpass.logPass
# print(f'dfsr                    {logpass.logPass.dfsr}')
#print(f'longStr                 {logpass.logPass.longStr}')
#print(f'type01Plan              {logpass.logPass.type01Plan}')
# lp.type01Plan.numChannels
#print(f'frameSetLongStr         {logpass.logPass.frameSetLongStr}')
# lp.frameSetLongStr()  # str or 'N/A'

# Not useful now
# print(f'curveUnitsAsStr         {logpass.logPass.curveUnitsAsStr}')
# print(f'curveUnits              {logpass.logPass.curveUnits}')
# print(f'frameFromX              {logpass.logPass.frameFromX}')
# print(f'hasOutpMnem             {logpass.logPass.hasOutpMnem}')
# print(f'outpMnemS               {logpass.logPass.outpMnemS}')
# print(f'retExtChIndexList       {logpass.logPass.retExtChIndexList}')

# Somente se lp.frameSet is not None
#print(f'genFrameSetHeadings     {logpass.logPass.genFrameSetHeadings}')
#print(f'genFrameSetScNameUnit   {logpass.logPass.genFrameSetScNameUnit}')

# Usado para criar um frameset
# print(f'setFrameSetChX          {logpass.logPass.setFrameSetChX}')
# print(f'setFrameSet             {logpass.logPass.setFrameSet}')
# print(f'genOutpPoints           {logpass.logPass.genOutpPoints}')
#print(f'jsonObject              {logpass.logPass.jsonObject}')

# lpdict = lp.jsonObject()
# numchannels = lpdict['Plan']['NumChannels']
# channels = lpdict['Channels']
# firstval = lpdict['Xaxis']['FirstValOptical']
# lastval = lpdict['Xaxis']['LastValOptical']
# totalframes = lpdict['Xaxis']['TotalFrames']
# spacing = lpdict['Xaxis']['SpacingOptical']
# units = lpdict['Xaxis']['UnitsOptical']
# 
# print('firstval lastval totalframes spacing units')
# 
# print(f'numchannels         {numchannels}')
# print(f'channels            {channels}')
# print(f'firstval            {firstval}')
# print(f'lastval             {lastval}')
# print(f'totalframes         {totalframes}')
# print(f'spacing             {spacing}')
# print(f'units               {units}')

# print('Reading logpasses')
# log_passes = list(lis_idx.genLogPasses())
# log_passes_len = len(log_passes)
# print(f'Found {log_passes_len} logpasses')
# 
# # Read dataset
# data = []
# for idx, log_pass in enumerate(log_passes):
#     print(f'Loading FrameSet: {idx+1:02d}/{log_passes_len}')
#     log_pass.logPass.setFrameSet(lis_file)
#     print(f'Found {1} channels and {1} datapoints')
#     data.append(log_pass.logPass.frameSet.frames)




# OLD CODE
# 
# for x in glob.glob(os.path.join(dirname, '*.dlis')): 
#     try: 
#         dlis = dlisio.load(x) 
#     except RuntimeError as e: 
#         print(f'{x:50s}: X') 
#     else:
#         print(f'{x:50s}: {len(dlis)}') 
