import os
import glob
import dlisio
import dlispy
#import LogicalFile, Object, Attribute, FrameData, PrivateEncryptedEFLR, parse

# JUST A TEST


dirname = 'data/input/dlis'
basename = 'ANP_1ELPS4PR_sta_148.1.dlis'

dlis_filepath = os.path.join(dirname, basename)

# try:
#     dlis = dlisio.load(dlis_filepath)
# except RuntimeError as e:
#     print(f'Error loading {dlis_filepath}')
# else:
#     print(f'{x:50s}: {len(dlis)}') 
# 
# output, logical_file_list = parse(dlis_filepath, eflr_only=False)

# OLD CODE

for x in glob.glob(os.path.join(dirname, '*.dlis')): 
    try: 
        dlis = dlisio.load(x) 
    except RuntimeError as e: 
        print(f'{x:50s}: X') 
    else:
        print(f'{x:50s}: {len(dlis)}') 
