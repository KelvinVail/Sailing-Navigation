import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
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

nrow = 3
ncol = 4

fig = plt.figure(figsize=(ncol+1, nrow+1))

gs = gridspec.GridSpec(nrow, ncol,
                       wspace=0.0, hspace=0.0,
                       top=1.-0.5/(nrow+1), bottom=0.5/(nrow+1),
                       left=0.5/(ncol+1), right=1-0.5/(ncol+1))


for i in range(nrow):
    for j in range(ncol):

        print(i, j)
        plt.subplot(gs[i,j])

        u = data.variables['var49'][i+j]
        v = data.variables['var50'][i+j]
        minutes = data.variables['time'][i+j]
        dt = datetime.datetime(1900,1,1) + datetime.timedelta(minutes=minutes)

        print(dt)
        speed = (u**2 + v**2) * 1.94384

        m = Basemap(resolution='c', projection='lcc',
                    lat_0 = np.min(lats) + ((np.max(lats)-np.min(lats))/2),
                    lon_0 = np.min(lons) + ((np.max(lons)-np.min(lons))/2),
                   llcrnrlon=np.min(lons),
                   llcrnrlat=np.min(lats),
                   urcrnrlon=np.max(lons),
                   urcrnrlat=np.max(lats))

        x, y = m(lons, lats)
        s = m.contourf(x, y, speed, 100, vmax=10)
        #cb = m.colorbar(s, 'bottom', size='5%', pad='2%')
        #cb.ax.tick_params(labelsize=24)
        #plt.title(str(dt) + ' UTC', fontsize=24)
        #m.drawcoastlines(linewidth=1.5)

        #m.quiver(x,y,u,v, scale=700)

plt.show()
