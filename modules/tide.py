import datetime
import math
import modules.navigation as nav
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


def tide_total(grib_path, wp_from, wp_to, start_time, speed):
    step_size = 0.25 # 15 minutes
    dist = nav.haversine_distance(wp_from, wp_to)
    bearing = nav.bearing(wp_from, wp_to)
    ETA_hr = dist / speed
    partial_step = None
    next_position = wp_from
    #if ETA is more than 15 minutes calculate total tide at 15 miunute steps
    if ETA_hr > step_size:
        steps = ETA_hr / step_size
        whole_steps = int(steps)
        partial_step = steps - whole_steps
        for step in range(0, whole_steps):
            time_from_start = start_time + datetime.timedelta(hours=(step *
                                                                     step_size))
            seconds_from_start = (step * step_size) * 3600
            step_position = nav.estimated_position(wp_from, bearing, speed,
                                                   seconds_from_start)
            tide_at_step = tide_forecast(grib_path, step_position[0],
                                         step_position[1], time_from_start)
            tide_during_step = tide_at_step[0] * step_size
            next_position = nav.estimated_position(next_position,
                                                   tide_at_step[1],
                                                   tide_during_step,
                                                   step_size * 3600)
            #print(time_from_start, next_position, tide_at_step)

    if partial_step != None or ETA_hr <= step_size:
        if ETA_hr <= step_size:
            step_size = ETA_hr
            time_from_start = start_time + datetime.timedelta(hours=step_size)
        else:
            step_size = ((whole_steps-1) * step_size) + (step_size * partial_step)
            time_from_start = start_time + datetime.timedelta(hours=step_size)
            step_size = partial_step

        seconds_from_start = (time_from_start - start_time).total_seconds()
        step_position = nav.estimated_position(wp_from, bearing, speed,
                                               seconds_from_start)
        tide_at_step = tide_forecast(grib_path, step_position[0],
                                     step_position[1], time_from_start)
        tide_during_step = tide_at_step[0] * step_size
        next_position = nav.estimated_position(next_position,
                                               tide_at_step[1],
                                               tide_during_step,
                                               step_size * 3600)
        #print(time_from_start, next_position, tide_at_step)

    return next_position
