import matplotlib.pyplot as plt
from pyproj import Geod
import matplotlib.path as mpath
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import shapely.geometry as sgeom

import cartopy.crs as ccrs

def circle(geod, lon, lat, radius, n_samples=360):
    """
    Return the coordinates of a geodetic circle of a given
    radius about a lon/lat point.

    Radius is in meters in the geodetic's coordinate system.

    """
    lons, lats, back_azim = geod.fwd(np.repeat(lon, n_samples),
                                     np.repeat(lat, n_samples),
                                     np.linspace(360, 0, n_samples),
                                     np.repeat(radius, n_samples),
                                     radians=False,
                                     )
    return lons, lats


def main():
    ax1 = plt.axes(projection=ccrs.Robinson())
    ax1.coastlines()

    geod = Geod(ellps='WGS84')

    radius_km = 50
    n_samples = 80

    ax1.add_feature(cfeature.LAND)
    ax1.add_feature(cfeature.OCEAN)
    ax1.add_feature(cfeature.COASTLINE)
    ax1.add_feature(cfeature.BORDERS, linestyle=':')

    # set extent to scandinavia
    lat1, lat2, lon1, lon2 = 54, 72, 4, 32

    ax1.set_extent([lon1, lon2, lat1, lat2], ccrs.Geodetic())

    geoms = []
    for lat in np.linspace(lat1, lat2, 10):
        for lon in np.linspace(lon1, lon2+10, 7):
            lons, lats = circle(geod, lon, lat, radius_km * 1e3, n_samples)
            geoms.append(sgeom.Polygon(zip(lons, lats)))

    ax1.add_geometries(geoms, ccrs.Geodetic(), facecolor='blue', alpha=0.7)

    ax1.gridlines()
    plt.show()




if __name__ == '__main__':
    main()

