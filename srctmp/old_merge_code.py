
    # lis.append(nlis)
    # agp.append(nagp)
    # lit.append(nlit)


# lis0 = lis[0]
# lit0 = lit[0]
# agp0 = agp[0]


#dept = lis0['DEPT'].iloc[0]
#rock_id = find_rock_id(agp0, dept)
#rock_name = lit0[lit0['id'] == rock_id]['lito'].iloc[0]


# Build LIS dataframes
# ldf = []
# for filename in input_filepath:
#     ldf.append(lis_to_dataframe(filename))

# Some sample selections
#lll = ldf[0][['DEPT', 'SP_4']]
#ppp = ldf[0].filter(regex='DEPT|SP.*')
#llln = lll[lll['SP_4'].notnull()]

# lito_ids_df = sys.argv[1]
# input_dir = sys.argv[2]
# Build input files
# VALID_FORMATS = [ '.lis' ]
# input_filepath = []
# for root, dirs, files in os.walk(input_dir):
#     path = root.split(os.sep)
#     for filename in files:
#         filesplit = os.path.splitext(filename)
#         if filesplit[-1] in VALID_FORMATS:
#             input_filepath.append(os.path.join(*path, filename))
# input_filepath.sort()

# some sample plotting
#lll.plot.scatter(x='DEPT', y='SP_4', s=0.1)
# llln.plot(x='DEPT')


# Sample Frame
#log_pass = log_passes_list[0]

# Redundant
# nframes =  log_pass.logPass.totalFrames  number of datapoints
# nchannels =  log_pass.logPass.type01Plan.numChannels
# diff_in_depth = df['DEPT'].diff()


# Load frameset data
#log_pass.logPass.setFrameSet(filehandler)

# channel_scheme = list(log_pass.logPass.genFrameSetScNameUnit())
# fields, units = list(zip(*channel_scheme))
# fields = [f.strip() for f in fields]
# units = [u.strip() for u in units]
#data = log_pass.logPass.frameSet.frames
# df = pd.DataFrame(data, columns=fields)
# df = df.replace(-999.25, np.nan)

# data[0, :] first capture
# data[:, 0] first channel




# for idx, record in enumerate(records):
#     print(idx, record)


# newfields = []
# for i, v in enumerate(fields):
#     totalcount = fields.count(v)
#     count = fields[:i].count(v)
#     newfields.append(v + '_' + str(count + 1) if totalcount > 1 else v)
# fields = newfields

# Read all files in path

# Build the dataset
# Write to some output
