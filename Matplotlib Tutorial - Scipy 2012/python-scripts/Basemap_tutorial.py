# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%pylab inline

# <headingcell level=1>

# Basic Plotting

# <markdowncell>

# Basemap is a toolkit for Matplotlib that facilitates plotting data on maps. Features:
# 
# * Reading in and displaying shapefiles
# * Plotting based on shapefile attributes
# * Wide variety of map projections
# * Warping images to projection
# * Plotting through Matplotlib's usual plot methods.
# * Manages ticking and aspect ratio

# <codecell>

from mpl_toolkits.basemap import Basemap
m = Basemap(-110, 25, -90, 40, projection='laea', lat_0=32.5, lon_0=-97, resolution='i')
m.drawcoastlines()
m.drawcountries()
m.drawstates()

# <codecell>

austin = (-97.754, 30.261)
austinX, austinY = m(*austin)
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.plot(austinX, austinY, marker='s')

# <codecell>

austinX, austinY

# <codecell>

m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.bluemarble()

# <codecell>

m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.bluemarble()

# Make a 1 degree grid
lon = np.arange(-110, -89, 1)
lat = np.arange(25, 45, 1)
lon,lat = np.meshgrid(lon, lat)
data = (lon - -100)**2 + (lat - 32)**2

x,y = m(lon, lat)
m.contour(x, y, data, 15)

# <headingcell level=2>

# EXERCISE:

# <markdowncell>

#  Make a plot of scattered random data (given) on an Lambert Conformal Conic (lcc) projection. Include ocean and country borders.

# <codecell>

t = np.linspace(0, 24)
vel = np.array([0.75, 0.25])[:, None] + np.random.randn(2, t.size)
pos = np.empty((2, t.size))
pos[:, 0] = [-97.754, 30.261]
for i in range(1, t.size):
    pos[:, i] = pos[:, i - 1] + vel[:, i] * (t[i] - t[i - 1])

# your code here

# <headingcell level=1>

# Advanced Features

# <codecell>

from datetime import datetime
m = Basemap(projection='mill', lon_0=180)
m.drawmapboundary(fill_color='royalblue')
m.drawcoastlines()
m.fillcontinents()
m.drawcountries()
CS = m.nightshade(datetime.utcnow())

# <headingcell level=2>

# Great circles

# <codecell>

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

# setup lambert azimuthal map projection.
# create new figure
fig=plt.figure()
m = Basemap(llcrnrlon=-100.,llcrnrlat=20.,urcrnrlon=20.,urcrnrlat=60.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='c',area_thresh=10000.,projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
#m = Basemap(llcrnrlon=-100.,llcrnrlat=20.,urcrnrlon=20.,urcrnrlat=60.,\
#            resolution='c',area_thresh=10000.,projection='gnom',\
#            lat_0=40.,lon_0=-45.)

# nylat, nylon are lat/lon of New York
nylat = 40.78
nylon = -73.98
# lonlat, lonlon are lat/lon of London.
lonlat = 51.53
lonlon = 0.08
# find 1000 points along the great circle.
#x,y = m.gcpoints(nylon,nylat,lonlon,lonlat,1000)
# draw the great circle.
#m.plot(x,y,linewidth=2)
# drawgreatcircle performs the previous 2 steps in one call.
m.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='b')
m.drawcoastlines()
m.fillcontinents()
# draw parallels
circles = np.arange(10,90,20)
m.drawparallels(circles,labels=[1,1,0,1])
# draw meridians
meridians = np.arange(-180,180,30)
m.drawmeridians(meridians,labels=[1,1,0,1])

# <headingcell level=2>

# Plotting custom shape file

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

# Lambert Conformal map of lower 48 states.
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

# State boundary data
# data from U.S Census Bureau
# http://www.census.gov/geo/www/cob/st2000.html
shp_info = m.readshapefile('st99_d00','states',drawbounds=True)
# population density by state from
# http://en.wikipedia.org/wiki/List_of_U.S._states_by_population_density
popdensity = {
'New Jersey':  438.00,
'Rhode Island':   387.35,
'Massachusetts':   312.68,
'Connecticut':    271.40,
'Maryland':   209.23,
'New York':    155.18,
'Delaware':    154.87,
'Florida':     114.43,
'Ohio':  107.05,
'Pennsylvania':  105.80,
'Illinois':    86.27,
'California':  83.85,
'Hawaii':  72.83,
'Virginia':    69.03,
'Michigan':    67.55,
'Indiana':    65.46,
'North Carolina':  63.80,
'Georgia':     54.59,
'Tennessee':   53.29,
'New Hampshire':   53.20,
'South Carolina':  51.45,
'Louisiana':   39.61,
'Kentucky':   39.28,
'Wisconsin':  38.13,
'Washington':  34.20,
'Alabama':     33.84,
'Missouri':    31.36,
'Texas':   30.75,
'West Virginia':   29.00,
'Vermont':     25.41,
'Minnesota':  23.86,
'Mississippi':   23.42,
'Iowa':  20.22,
'Arkansas':    19.82,
'Oklahoma':    19.40,
'Arizona':     17.43,
'Colorado':    16.01,
'Maine':  15.95,
'Oregon':  13.76,
'Kansas':  12.69,
'Utah':  10.50,
'Nebraska':    8.60,
'Nevada':  7.03,
'Idaho':   6.04,
'New Mexico':  5.79,
'South Dakota':  3.84,
'North Dakota':  3.59,
'Montana':     2.39,
'Wyoming':      1.96,
'Alaska':     0.42}
# choose a color for each state based on population density.
colors={}
statenames=[]
cmap = plt.cm.hot # use 'hot' colormap
vmin = 0; vmax = 450 # set range.
print m.states_info[0].keys()
for shapedict in m.states_info:
    statename = shapedict['NAME']
    # skip DC and Puerto Rico.
    if statename not in ['District of Columbia','Puerto Rico']:
        pop = popdensity[statename]
        # calling colormap with value between 0 and 1 returns
        # rgba value.  Invert color range (hot colors are high
        # population), take sqrt root to spread out colors more.
        colors[statename] = cmap(1.-np.sqrt((pop-vmin)/(vmax-vmin)))[:3]
    statenames.append(statename)
# cycle through state names, color each one.
ax = plt.gca() # get current axes instance
for nshape,seg in enumerate(m.states):
    # skip DC and Puerto Rico.
    if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
        color = rgb2hex(colors[statenames[nshape]]) 
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)
# draw meridians and parallels.
m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])
plt.title('Filling State Polygons by Population Density')

