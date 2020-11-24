import pandas as pd

dfA = pd.DataFrame([[10.3, 3, 1],
                    [13.5, 2, 3],
                    [15.2, 1, 2]],
                   columns=['X', 'A', 'B'])
# dfA.set_index('X', inplace=True)

dfB = pd.DataFrame([[11.1, 2, 0],
                    [13.5, 3, 1],
                    [16.8, 4, 4]],
                   columns=['X', 'C', 'D'])
#dfB.set_index('X', inplace=True)

dfO = pd.merge(dfA, dfB, how='outer')
dfO.sort_values('X', inplace=True)
