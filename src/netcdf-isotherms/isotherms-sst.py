'''
Monthly Mean of Sea Surface Temperature
Plot yearly isotherms for 1854 - 2017
Calculate mean latitude of 13oC isotherm
Data source: https://www.esrl.noaa.gov/psd/cgi-bin/DataAccess.pl?DB_dataset=NOAA+Extended+Reconstructed+SST+V4&DB_variable=Sea+Surface+Temperature&DB_statistic=Mean&DB_tid=60700&DB_did=168&DB_vid=4133
Coordinates: 48.5N-52.5N, 12.5W-4.5W 
Area: Celtic Sea
Author: Olga Lyashevska
'''

#!/usr/bin/env python
import netCDF4 
from netCDF4 import num2date
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
from matplotlib import _cntr as cntr
import os

# set working dir
os.chdir('/home/olga/Documents/nuig-doyle/')

# read in
nc_f = netCDF4.Dataset('data/sst/X193.1.57.1.256.2.57.28.nc')

print nc_f
print nc_f.file_format

# plot area
fig = plt.figure()
fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9)
m = Basemap(projection='merc', 
            lat_0 =  50, 
            lon_0 = -10,
            resolution = 'i', 
            area_thresh = 0.05,
            llcrnrlon= -12.5, 
            llcrnrlat=48.5, 
            urcrnrlon=-4.5, 
            urcrnrlat=52.5)

m.drawcoastlines(linewidth = 0.2, zorder = 0)
m.fillcontinents(color='coral',lake_color='aqua')

#m.contour(x, y, z)
#c = cntr.Cntr(x, y, z)
#
## trace a contour at sst == 13
#res = c.trace(10)

sst = nc_f.variables['sst'][:]

# plot a histogram of sst
meansst = sst[:].mean(axis = (1,2))
plt.hist(meansst, bins=256, fc='k', ec='k')

# time 
times = nc_f.variables['time']
dates = num2date(times[:],times.units)
print('starting date = %s' % dates[0])
print('ending date = %s'% dates[-1])
start = dates[0].year
end = dates[-1].year
     
nx, ny = sst.shape[2], sst.shape[1]
lons, lats = m.makegrid(nx,ny)
x, y = lons, lats

# plot average over whole period
z=sst.mean(axis=0)
z = np.flipud(z)
plt.figure()
CS = plt.contour(x,y,z,linestyles='dashed')
plt.clabel(CS, inline=1, fontsize=10)
plt.title('%s - %s' %(start, end))
plt.xlabel('Lon')
plt.ylabel('Lat')
plt.savefig('figs/isoterms/{start}-{end}.png'.format(start=start, end=end))


# plot yearly average
# calculate mean latitude of 13oC isotherm

iso13 = {}
keys = range(start,end)
i = 0
for year in range(start,end):
  z = sst[i:(i+12)].mean(axis=0)
  z = np.flipud(z)
  plt.figure()
  CS = plt.contour(x, y, z, linestyles='dashed')
  plt.clabel(CS, inline=1, fontsize=10)
  plt.title('%s' % year)
  plt.xlabel('Lon')
  plt.ylabel('Lat')
  # extract data from a single contour
  c = cntr.Cntr(x, y, z)
  # trace a contour at sst == 13
  ctrace = c.trace(13)
  # take average of lat
  if len(ctrace)!=0:
    ctracey = ctrace[0][:,1].mean()
  else:
    ctracey=np.nan
  iso13[year] = ctracey
  #plt.savefig('figs/isoterms/{year}.png'.format(year=year))
  i += 12


plt.figure()
plt.plot(*zip(*sorted(iso13.items())), marker = 'o', ls = '--', color = 'r', ms=3)
plt.title('Mean latitude of 13oC isotherm')
plt.xlabel('Year')
plt.ylabel('Mean Lat')
plt.savefig('figs/isoterms/meanlat13oC.png')

# save iso13 
dfiso13 = pd.DataFrame(iso13.items(), columns=['year', 'iso13'])
dfiso13.to_csv('data/sst/iso13.csv')

