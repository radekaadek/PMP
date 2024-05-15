# this script is used to guess the EPSG code of a projection
# it uses the pyproj library to do the guessing
# goes through all the EPSG codes and tries to find the one that produces the least error
# for a given mathematically defined projection

import pyproj
import numpy as np
import sys

def odwzorowanie(Lk, Fk):
    R = 6371e3
    Lk = np.deg2rad(Lk)
    Fk = np.deg2rad(Fk)
    lam0 = 0
    phi0 = 90
    lam_rad = np.deg2rad(lam0)
    phi_rad = np.deg2rad(phi0)
    ror = R * 1/np.tan(phi_rad) + R * phi_rad
    c = np.sin(phi_rad)
    ro = ror - R * Fk
    delta = c * (Lk - lam_rad)
    Xk = -ro * np.cos(delta)
    Yk = ro * np.sin(delta)
    return Xk, Yk

def guess_eps(projection):
    current_error = np.inf
    curr_epsg = None
    best_error = np.inf
    latlon_proj = pyproj.Proj('EPSG:4326')
    for epsg in range(102000, 104000):
        try:
            p = pyproj.Proj(f'ESRI:{epsg}')
            transformation = pyproj.Transformer.from_proj(latlon_proj, p)
            error = 0
            for x in np.linspace(-np.pi/2, np.pi/2, 50):
                for y in np.linspace(-np.pi, np.pi, 50):
                    x_lat = np.rad2deg(x)
                    y_lon = np.rad2deg(y)
                    x1, y1 = projection(x, y)
                    x2, y2 = transformation.transform(x_lat, y_lon)
                    error += (x1-x2)**2 + (y1-y2)**2
            if error < current_error:
                current_error = error
                curr_epsg = epsg
                best_error = error
                print(f'Current best guess: {curr_epsg}')
        except Exception as e:
            print(f"{e}: EPSG {epsg} not found")
            pass
    return curr_epsg, best_error


epsg, err = guess_eps(odwzorowanie)
print('The guessed code is: {}'.format(epsg))
print('The error is: {}'.format(err))

# now try +proj=omerc +lat_0=40 +lat_1=0 +lon_1=0 +lat_2=60 +lon_2=60 +k=1 +x_0=0 +y_0=0 +R=6371000 +units=m +no_defs
# lat1, lon1 = 0.0001, 0.0001
# proj = pyproj.Proj(f'+proj=omerc +lat_0=40 +lat_1={lat1} +lon_1={lon1} +lat_2=60 +lon_2=60 +k=1 +x_0=0 +y_0=0 +R=6371000 +units=m +no_defs')
# latlon_proj = pyproj.Proj('EPSG:4326')
# transformation = pyproj.Transformer.from_proj(latlon_proj, proj)
# error = 0
# x1, y1 = 0, 0
# for x in np.linspace(-np.pi/2, np.pi/2, 100):
#     for y in np.linspace(-np.pi, np.pi, 100):
#         x_lat = np.rad2deg(x)
#         y_lon = np.rad2deg(y)
#         x1, y1 = custom_projection(x, y, lat1, lon1)
#         x2, y2 = transformation.transform(x_lat, y_lon)
#         error += (x1-x2)**2 + (y1-y2)**2
#         print(f'x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}')
# print('The error for the given projection is: {}'.format(error))

import matplotlib.pyplot as plt
plt.figure(1)
plt.axis('equal')
A = np.loadtxt('kontynenty.txt')
Lk = A[:, 0]
Fk = A[:, 1]
# xs = np.array(Lk)
# ys = np.array(Fk)

Xs, Ys = odwzorowanie(Lk, Fk)
plt.plot(Xs, Ys, '.', markersize=4)
plt.show()
