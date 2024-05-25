from sympy import Symbol, cos, sin, cot, atan2, atan

F = Symbol('F')
F0 = Symbol('F0')
L = Symbol('L')
L0 = Symbol('L0')
R = Symbol('R')

X = -R * (cot(F0) + F0 - F) * cos(sin(F0) * (L - L0))
Y = R * (cot(F0) + F0 - F) * sin(sin(F0) * (L - L0))

dX_dF = X.diff(F)
dY_dF = Y.diff(F)
dX_dl = X.diff(L)
dY_dl = Y.diff(L)

print(f"{dX_dF=}")
print(f"{dY_dF=}")
print(f"{dX_dl=}")
print(f"{dY_dl=}")



