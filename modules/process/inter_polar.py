import pandas as pd
import numpy as np


FILE_PATH = 'raw_polar.csv'

df = pd.DataFrame.from_csv(FILE_PATH)
df.reset_index(inplace=True)
df.set_index(['SWS', 'SWA'], inplace=True)
df = df.interpolate()
df = df.replace(0, np.nan)

df.reset_index(inplace=True)
df.loc[df['SWS'] == 1, 'boat_speed'] = 0
df = df.sort(['SWA', 'SWS'])
df.set_index(['SWA', 'SWS'], inplace=True)
df = df.interpolate()

#df.reset_index(inplace=True)
#df.loc[df['SWS'] > 20, 'boat_speed'] = np.nan
#df = df.sort(['SWS', 'SWA'])
#df.set_index(['SWS', 'SWA'], inplace=True)
#df = df.interpolate()

df = df.unstack(level=1)
print(df.head())
df.to_csv('inter_polar.csv')
