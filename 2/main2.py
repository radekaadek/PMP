import matplotlib.pyplot as plt
import numpy as np

# get data from kontynenty.txt
xs = []
ys = []

with open("kontynenty.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        x, y = line.split()
        # if np.degrees(-np.pi/2) <= float(x) <= np.degrees(np.pi/2) and np.degrees(-np.pi) <= float(y) <= np.degrees(np.pi):
        xs.append(float(x))
        ys.append(float(y))

xs = np.deg2rad(np.array(xs))
ys = np.deg2rad(np.array(ys))
xs, ys, = ys, xs

# plot the projection:
R = 6371e3
F0 = np.radians(90)
L0 = 0
ror = R*(1/np.tan(F0)) + R*F0
c = np.sin(F0)
ro = ror - R*xs
delta = c*(ys - L0)
X = -ro*np.cos(delta)
Y = ro*np.sin(delta)



fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.plot(X, Y, 'o', markersize=1)
plt.show()

