import datetime
import math
import numpy as np
import pygrib
from netCDF4 import Dataset


def wind_forecast_nc(file_path, lat, lon, time_stamp):
    time_stamp_dec = int(time_stamp.strftime('%Y%m%d'))
    secs = (time_stamp.hour*3600 + time_stamp.minute*60 +
            time_stamp.second)/86400.0
    time_stamp_dec += secs

    data = Dataset(file_path)
    lats = data.variables['lat'][:]
    lons = data.variables['lon'][:]
    time = data.variables['time'][:]

    lat_idx = np.abs(lats - lat).argmin()
    lon_idx = np.abs(lons - lon).argmin()
    #TODO
    #time is set as hours since forecast
    #figure out how to get forecast time from file
    time_stamp_dec = 99
    time_idx = np.abs(time - time_stamp_dec).argmin()

    v = data.variables['var33'][time_idx, lat_idx, lon_idx]
    u = data.variables['var34'][time_idx, lat_idx, lon_idx]
    print(v, u)
    v = round(v - (v*2), 2)
    u = round(u - (u*2), 2)
    print(v, u)
    print(time)

    h = round(math.sqrt(v**2 + u**2) * 1.94384, 2)
    d = int(round(math.degrees(math.atan2(v, u))%360, 2))

    return h, d


def wind_forecast_grib(file_path, lat, lon, time_stamp):
    lat = 50.784
    lon = -1.297
    grib_path = \
    '/home/kelvin/Documents/Navigation/Gribs/Tide/AROME_0.01_SP1_00H_201705061200.grib2'
    grbs = pygrib.open(grib_path)
    #for grb in grbs:
    #    print(grb.parameterName)

    grb = grbs.select(parameterName='v-component of wind')[0]    
    lats, lons = grb.latlons()
    v_data = grb.values
    #v_data, lats, lons = grb.data(lat1=50, lat2=51, lon1=-2,
    #                            lon2=-1)

    grb = grbs.select(parameterName='u-component of wind')[0]    
    u_data = grb.values
    #u_data, lats, lons = grb.data(lat1=50, lat2=51, lon1=-2,
    #                            lon2=-1)

    grb = grbs.select(parameterName='Temperature')[0]    
    t_data = grb.values
    #t_data, lats, lons = grb.data(lat1=50, lat2=51, lon1=-2,
    #                            lon2=-1)

    print(v_data.shape)
    lon_idx = np.abs(lons - lon).argmin()
    lat_idx = np.abs(lats[:,lon_idx] - lat).argmin()
    v = v_data[lat_idx, lon_idx]
    u = u_data[lat_idx, lon_idx]
    t = t_data[lat_idx, lon_idx]
    print(v, u, t)
    print(lats[lat_idx, lon_idx], lons[lat_idx, lon_idx])
    v = v - (v*2)
    u = u - (u*2)

    h = math.sqrt(v**2 + u**2) * 1.94384
    print(h)
    d = math.degrees(math.atan2(u, v))%360
    print(d)
