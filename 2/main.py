import matplotlib.pyplot as plt
from pyproj import Geod
import matplotlib.path as mpath
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pyproj
import shapely.geometry as sgeom

import cartopy.crs as ccrs

def main():

    # # set extent to the whole world
    # lat1, lat2, lon1, lon2 = -90, 90, -180, 180
    # now set extent to Europe
    # lat1, lat2, lon1, lon2 = 35, 75, -20, 45
    # lat0 = (lat1 + lat2) / 2
    # lon0 = (lon1 + lon2) / 2

    lat1, lat2, lon1, lon2 = -90, 90, -180, 180
    lat0 = 0.000001
    lon0 = 0
    # set a spherical globe with R=6371 km
    sphere = ccrs.Globe(semimajor_axis=6371e3, semiminor_axis=6371e3, ellipse='sphere')
    proj = ccrs.AzimuthalEquidistant(central_latitude=lat0, central_longitude=lon0, globe=sphere)
    # proj = ccrs.AlbersEqualArea(central_latitude=lat0, central_longitude=lon0, globe=sphere)


    ax1 = plt.axes(projection=proj)

    ax1.add_feature(cfeature.LAND)
    ax1.add_feature(cfeature.OCEAN)
    ax1.add_feature(cfeature.COASTLINE)
    ax1.add_feature(cfeature.BORDERS, linestyle=':')
    ax1.gridlines(draw_labels=True, color='black', alpha=1, linestyle='-.')

    # ax1.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
    
    # ax1.tissot(facecolor='orange', alpha=0.4, lons=np.linspace(lon1, lon2, 5), lats=np.linspace(lat1, lat2, 10), rad_km=150)
    ax1.tissot(facecolor='orange', alpha=0.4, lons=np.linspace(lon1, lon2, 20), lats=np.linspace(lat1, lat2, 15), rad_km=500)


    ax1.gridlines()
    plt.show()




if __name__ == '__main__':
    main()

