import pandas as pd
import numpy as np

df = pd.DataFrame([[10.3, 3,      1, np.nan, np.nan],
                   [13.5, np.nan, 3, 2     , np.nan],
                   [15.2, 1,      2, 2     , 3 ]],
                   columns=['X', 'A', 'B', 'A', 'A'])

seen = {}
dupes = []

fields = df.columns
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


