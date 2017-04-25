import pandas as pd
import numpy as np


FILE_PATH = 'raw_polar.csv'
SWS = 0
boat_speed = None

with open(FILE_PATH, 'rw') as f:
    with open('prep_polar.csv', 'w') as w:
        #w.write('SWA,SWS,boat_speed')
        for line in f:
            SWA, SWS, boat_speed = line.split(',')
            if SWA != 'SWA':
                if len(boat_speed) > 1:
                    last_boat_speed = boat_speed
                if int(SWA) == 180:
                    boat_speed = last_boat_speed
            w.write(SWA + ',' + SWS + ',' +  boat_speed)

df = pd.DataFrame.from_csv('prep_polar.csv')
df.reset_index(inplace=True)
df.set_index(['SWS', 'SWA'], inplace=True)
df = df.interpolate()
df = df.replace(0, np.nan)

df.reset_index(inplace=True)
df.loc[df['SWS'] == 0, 'boat_speed'] = 0
df.loc[df['SWA'] == 0, 'boat_speed'] = 0

df.set_index(['SWS', 'SWA'], inplace=True)

df = df.unstack(level=1)
df = df.interpolate()
df = df.stack()
df.to_csv('inter_polar.csv')
