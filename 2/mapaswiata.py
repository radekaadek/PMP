# translate to python
# clear all;
# R=6371;
# L0=0;
# %generowanie macierzy punktow wezlowych siatki
# no_f=181;
# no_l=361;
# f=linspace(-pi/2,pi/2,no_f);
# l=linspace(-pi,pi,no_l);
# [L,F] = meshgrid(l,f);
#
# %wzor na odwzorowanie
# X=R*F;
# Y=R*cos(F).*(L-L0);
#
# %parametry rysowania
# figure(1);
# axis equal;
# hold on;
#
# %rysowanie siatki
# delta_f=15;
# for i=1:delta_f:no_f;
#     plot(Y(i,:),X(i,:),'b');
# end
# delta_l=30;
# for i=1:delta_l:no_l;
#     plot(Y(:,i),X(:,i),'b');
# end
#
# %odczytywanie wspolrzednych (fi,lambda) kontynent�w
# fid = fopen('kontynenty.txt','r');
# [A,inf] = fscanf(fid,'%f %f',[2 inf]);
# Lk=(A(1,:))*pi/180;
# Fk=(A(2,:))*pi/180;
#
# %wzor na odwzorowanie
# Xk=R*Fk;
# Yk=R*cos(Fk).*(Lk-L0);
#
# %wrysowanie kontynentow
# plot(Yk,Xk,'.','MarkerSize',4);

def odwzorowanie(Lk, Fk):
    R = 6371
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

import numpy as np
import matplotlib.pyplot as plt


# # generowanie macierzy punktów węzłowych siatki
# no_f = 181
# no_l = 361
# f = np.linspace(-90, 90, no_f)
# l = np.linspace(-180, 180, no_l)
# L, F = np.meshgrid(l, f)
#
# # wzór na odwzorowanie
# X, Y = odwzorowanie(L, F)

# parametry rysowania
plt.figure(1)
plt.axis('equal')

# # rysowanie siatki
# delta_f = 15
# for i in range(0, no_f, delta_f):
#     plt.plot(Y[i, :], X[i, :], 'b')
#
# delta_l = 30
# for i in range(0, no_l, delta_l):
#     plt.plot(Y[:, i], X[:, i], 'b')

# odczytywanie współrzędnych (fi, lambda) kontynentów
A = np.loadtxt('kontynenty.txt')
Lk = A[:, 0]
Fk = A[:, 1]

# wzór na odwzorowanie
# Xk = R * Fk
# Yk = R * np.cos(Fk) * (Lk - L0)


Xk, Yk = odwzorowanie(Lk, Fk)

# wrysowanie kontynentów
plt.plot(Yk, Xk, '.', markersize=4)
plt.show()

