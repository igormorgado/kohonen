import pandas as pd

df = pd.DataFrame([[0.5, 3], [1.0, 4], [1.3, np.nan], [2, 3], [2.4, 5], [3, np.nan]], columns=['X', 'Y'])
df.set_index('X', inplace=True)
