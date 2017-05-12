import datetime
import math
import numpy as np
import pygrib
from netCDF4 import Dataset


def wind_forecast_nc(file_path, lat, lon, time_stamp):

    data = Dataset(file_path)

    forecast_d, forecast_t = \
        data.variables['time'].getncattr('units').split(' ')[-2:]
    forecast_time = datetime.datetime(int(forecast_d.split('-')[0]),
                                      int(forecast_d.split('-')[1]),
                                      int(forecast_d.split('-')[2]),
                                      int(forecast_t.split(':')[0]),
                                      int(forecast_t.split(':')[1]),
                                      int(forecast_t.split(':')[2]))

    unit_time = round(((time_stamp - forecast_time).total_seconds()) / 3600, 2)

    lats = data.variables['lat'][:]
    lons = data.variables['lon'][:]
    time = data.variables['time'][:]

    lat_idx = np.abs(lats - lat).argmin()
    lon_idx = np.abs(lons - lon).argmin()
    time_idx = np.abs(time - unit_time).argmin()

    v = data.variables['var33'][time_idx, lat_idx, lon_idx]
    u = data.variables['var34'][time_idx, lat_idx, lon_idx]
    v = v - (v*2)
    u = u - (u*2)

    h = round(math.sqrt(v**2 + u**2) * 1.94384, 1)
    d = int(round(math.degrees(math.atan2(v, u))%360, 0))

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
