import datetime
import math
import numpy as np
from netCDF4 import Dataset


def tide_forecast(grib_path, lat, lon, time_stamp):
    #solent bouds: -1.828,50.477,-0.79,51
    if lon <= -1.823 or lon >= -0.79 or lat <= 50.477 or lat >= 51:
        file_name = 'english-channel-currents.nc'
    else:
        file_name = 'solent-currents.nc'

    grib_path += file_name

    time_stamp_dec = int(time_stamp.strftime('%Y%m%d'))
    secs = (time_stamp.hour*3600 + time_stamp.minute*60 +
            time_stamp.second)/86400.0
    time_stamp_dec += secs

    total_minutes = (time_stamp - datetime.datetime(1900, 1,
                                                    1)).total_seconds()/60

    data = Dataset(grib_path)
    time_units = data.variables['time'].getncattr('units')
    if time_units == 'minutes since 1900-1-1 00:00:00':
        set_time = total_minutes
    else:
        set_time = time_stamp_dec

    lats = data.variables['lat'][:]
    lons = data.variables['lon'][:]
    time = data.variables['time'][:]

    lat_idx = np.abs(lats - lat).argmin()
    lon_idx = np.abs(lons - lon).argmin()
    time_idx = np.abs(time - set_time).argmin()

    v = data.variables['var49'][time_idx, lat_idx, lon_idx]
    u = data.variables['var50'][time_idx, lat_idx, lon_idx]

    h = round(math.sqrt(v**2 + u**2) * 1.94384, 1)
    d = round(math.degrees(math.atan2(v, u))%360, 0)

    if not math.isnan(d):
        d = int(d)

    return h, d
