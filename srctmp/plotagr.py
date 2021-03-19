import matplotlib.pyplot as plt

prefixes = []
for well in lis:
    prefixes.extend(list(set([ x.split('_')[0] for x in sorted(list(well.columns))])))

# Estes campos não devem ser filtrados
prefixes.remove('LITO')
prefixes.remove('RIDS')
prefixes.remove('DEPT')

LIS = lis[0].copy()

# Drop Lito inexistente
LIS = LIS[LIS['LITO'].notna()]
print(prefixes)

# Interpola entre multiplas RUNS
for pref in prefixes:
    #print(pref)
    regex_str = f'{pref}_[0-9]+'
    LIS[pref] = LIS.filter(regex=regex_str).mean(axis=1)
    drop_columns = LIS.filter(regex=regex_str).columns
    #print(f"DROP COLUMNS {drop_columns}")
    LIS.drop(columns=drop_columns, inplace=True)

# Remove colunas que são somente NaNs 
LIS.dropna(axis=1, how='all', inplace=True)

# Interpola em profundidade
LIS.set_index('DEPT',inplace=True)
LIS.interpolate(method='values', inplace=True)
LIS.reset_index(inplace=True)

# Remove todas as linhas que são somente NAN
LIS.dropna(axis=0, how='all', inplace=True)
