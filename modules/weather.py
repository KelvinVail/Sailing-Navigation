import math
import numpy as np
import pygrib


lat = 50.784
lon = -1.297
grib_path = \
'/home/kelvin/Documents/Navigation/Gribs/Tide/AROME_0.01_SP1_03H_201705061200.grib2'
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
d = math.degrees(math.atan2(u, v))
print(d)
