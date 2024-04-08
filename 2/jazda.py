import numpy as np

R = 6371
L = 100
L0 = 100
F = 0.1


# Obliczenie miar zniekształceń odwzorowawczych
x_fi = R
y_fi = -R * (L - L0) * np.sin(F)
x_l = 0
y_l = R * np.cos(F)

Ep = x_fi ** 2 + y_fi ** 2
Fp = x_fi * x_l + y_fi * y_l
Gp = x_l ** 2 + y_l ** 2
Hp = np.abs(x_fi * y_l - y_fi * x_l)

Pd = Ep / (R ** 2)
Rd = Gp / (R ** 2 * np.cos(F) ** 2)

# skala pól
p = Hp / (R ** 2 * np.cos(F))

A = np.sqrt(Pd + Rd + 2 * p)
B = np.sqrt(np.abs(Pd + Rd - 2 * p))
# skale ekstremalne
m = 0.5 * (A + B)
n = 0.5 * (A - B)

# zniekształcenia kątowe
zk = 360 * np.abs(np.arctan((n - m) / (2 * np.sqrt(p)))) / np.pi

print(f'Pole powierzchni: {Pd}')
print(f'Pole powierzchni: {Rd}')
print(f'Skala pola: {p}')
print(f'Skala pól: {A}')
print(f'Skala pól: {B}')
print(f'Skala ekstremalna: {m}')
print(f'Skala ekstremalna: {n}')
print(f'Zniekształcenia kątowe: {zk}')

