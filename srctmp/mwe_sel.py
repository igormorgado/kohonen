import pandas as pd
import numpy as np

klasses_df = pd.DataFrame([[1, 'Sad'],
                           [7, 'Regular'],
                           [13, 'Happy'],
                           [42, 'Magical']],
                           columns=['klass', 'mood'])
                           
bins_df = pd.DataFrame([[0.0, 3.0, 1],
                        [3.0, 6.0, 7],
                        [6.0, 8.0, 13]],
                       columns=['lower', 'upper', 'klass'])


person_df = pd.DataFrame([['John', 1.5],
                          ['Mary', 3.6],
                          ['Paul', 7.2],
                          ['Josh', 5.7],
                          ['Phil', 9.9]],
                         columns=['name', 'feeling'])

# Want a final dataframe like:
#final_df = pd.DataFrame([['John', 1.5, 1, 'Sad'],
#                        ['Mary', 3.6, 7, 'Regular'],
#                        ['Paul', 7.2, 13, 'Happy'],
#                        ['Josh', 5.7, 7, 'Regular'],
#                        ['Phil', 9.9, 0, None]],
#                       columns=['name', 'feeling', 'klass', 'mood'])


def find_klass_from_feeling(feeling, bin_data):
    values = bin_data.values
    klass = values[(values[:,0] <= feeling) & (feeling <= values[:,1])][:,2]
    if len(klass) == 0:
        return 0
    else:
        return int(klass.flatten()[0])

def find_mood_from_class(klass, klasses_data):
    if klass == 0:
        return None
    retval = klasses_df[klasses_df['klass'] == klass]['mood'].iloc[0]
    return retval

# Based in each row from person_df feeling column, look in which bin it fall
# into, then based on bin klass returrn the correct mood from the class. The
# final dataframe will be added with `klass` and `mood` string.
final_df = person_df.copy()
klss = []
moods = []
for idx, row in person_df.iterrows():
    kls = find_klass_from_feeling(row['feeling'], bins_df)
    mood = find_mood_from_class(kls, klasses_df)
    klss.append(kls)
    moods.append(mood)
    
final_df['klass'] = klss
final_df['mood'] = moods

