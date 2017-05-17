import numpy as np
import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset


nc_file = \
'/home/kelvin/github/Sailing-Navigation/race_details/RORC_De_Guingand_Bowl_Race_2017/Grib/Tide/solent-currents.nc'
data = Dataset(nc_file)

lats = data.variables['lat'][:]
lons = data.variables['lon'][:]
time = data.variables['time'][:]

lons, lats = np.meshgrid(lons,lats)


for i in range(25):
    print(i)
    plt.subplot(5, 5, i+1)

    u = data.variables['var49'][i]
    v = data.variables['var50'][i]
    minutes = data.variables['time'][i]
    dt = datetime.datetime(1900,1,1) + datetime.timedelta(minutes=minutes)

    speed = (u**2 + v**2) * 1.94384

    m = Basemap(resolution='c', projection='lcc',
                lat_0 = np.min(lats) + ((np.max(lats)-np.min(lats))/2),
                lon_0 = np.min(lons) + ((np.max(lons)-np.min(lons))/2),
               llcrnrlon=np.min(lons),
               llcrnrlat=np.min(lats),
               urcrnrlon=np.max(lons),
               urcrnrlat=np.max(lats))

    x, y = m(lons, lats)
    s = m.contourf(x, y, speed, 1000, vmax=10)
    cb = m.colorbar(s, 'bottom', size='5%', pad='2%')
    #cb.ax.tick_params(labelsize=24)
    plt.title(str(dt) + ' UTC', fontsize=24)
    #m.drawcoastlines(linewidth=1.5)

    #m.quiver(x,y,u,v, scale=700)

plt.show()
