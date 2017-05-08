import datetime
import math
import numpy as np
from netCDF4 import Dataset


grib_path = '/home/kelvin/Documents/Navigation/Gribs/Tide/solent-sample.nc'
lat = 50.784
lon = -1.297
time_stamp = datetime.datetime(2016, 6, 30, 6, 00, 0)
time_stamp_dec = int(time_stamp.strftime('%Y%m%d'))
secs = (time_stamp.hour*3600 + time_stamp.minute*60 +
        time_stamp.second)/86400.0
time_stamp_dec += secs

data = Dataset(grib_path)
lats = data.variables['lat'][:]
lons = data.variables['lon'][:]
time = data.variables['time'][:]
#for item in time:
#    print(item)

lat_idx = np.abs(lats - lat).argmin()
lon_idx = np.abs(lons - lon).argmin()
time_idx = np.abs(time - time_stamp_dec).argmin()

v = data.variables['var49'][time_idx, lat_idx, lon_idx]
u = data.variables['var50'][time_idx, lat_idx, lon_idx]

print(v, u)
h = math.sqrt(v**2 + u**2) * 1.94384
print(h)
d = math.degrees(math.atan2(v, u))%360
print(d)
