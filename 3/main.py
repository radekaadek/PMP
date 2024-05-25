import numpy as np
from pyproj import Geod
import pyproj

R = 6371e3

def projection(lat, lon, lat0, lon0):
    R = 6371e3
    ror = R*(1/np.tan(np.radians(lat0))) + R*np.radians(lat0)
    c = np.sin(np.radians(lat0))
    ro = ror - R*np.radians(lat)
    delta = c*np.radians(lon - lon0)
    x = -ro*np.cos(delta)
    y = ro*np.sin(delta)
    return y, x

# define 2 points on a sphere and calculate the distance between them
name1, name2 = "Innsbruck", "Vienna"
lat1, lon1 = 47.280407, 11.409991 # Innsbruck
lat2, lon2 = 48.201961, 16.3646931 # Vienna
lat0, lon0 = lat1+lat2/2, lon1+lon2/2

# calculate distance between 2 points
# define geod as a sphere
geod = Geod(ellps="sphere", a=R, b=R)
# geod = Geod(ellps="WGS84")
angle1, angle2, distance_m = geod.inv(lon1, lat1, lon2, lat2)
print(f"2. Distance between {name1} and {name2}: {distance_m/1000:.2f} km")
# calcualte the distance using the formula: https://en.wikipedia.org/wiki/Great-circle_distance
dist = 6371 * np.arccos(np.sin(np.radians(lat1)) * np.sin(np.radians(lat2)) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.cos(np.radians(lon1) - np.radians(lon2)))
print(f"Distance between {name1} and {name2} using the formula: {dist:.2f} km")

print(f"Azimuth {name1}->{name2}: {angle1:.2f} deg, Azimuth {name2}->{name1}: {angle2:.2f} deg")

# calcualte angles in a triangle: north pole, Innsbruck, Vienna
inssbruck_angle = abs(angle1)
vienna_angle = abs(angle2)
north_pole_angle = abs(lon1 - lon2)
print(f"3. Angles in the triangle: {name1}: {inssbruck_angle:.2f} deg, {name1}: {vienna_angle:.2f} deg, North pole: {north_pole_angle:.2f} deg")

# now convert the points to a plane using the Lambert azimuthal equidistant projection on a sphere
# define the projection
sphere_proj = pyproj.Proj(proj="longlat", a=R, b=R, units="m")
aeqd_proj = pyproj.Proj(proj="aeqd", lat_0=lat0, lon_0=lon0, a=R, b=R, units="m")
# convert the points to the plane
transformer = pyproj.Transformer.from_proj(sphere_proj, aeqd_proj)
x1, y1 = transformer.transform(lon1, lat1)
x2, y2 = transformer.transform(lon2, lat2)

x1, y1 = projection(lat1, lon1, lat0, lon0)
x2, y2 = projection(lat2, lon2, lat0, lon0)

print(f"4.1 {name1} on the projection plane: ({x1:.2f}, {y1:.2f}), {name2} on the projection plane: ({x2:.2f}, {y2:.2f})")

distance_plane = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
print(f"4.2 Distance between {name1} and {name2} on the plane: {distance_plane/1000:.2f} km")
dist_diff = distance_plane - distance_m
print(f"4.3 Difference between the distances: {abs(dist_diff)/1000:.2f} km")

# calculate A12T and A21T
A12T = np.degrees(np.arctan2(y2 - y1, x2 - x1))
A21T = np.degrees(np.arctan2(y1 - y2, x1 - x2))
print(f"4.4 Topographic azimuths: A12T: {abs(A12T):.2f} deg, A21T: {abs(A21T):.2f} deg")

# calculate the convergence of meridians
# dX_dF=R*cos((L - L0)*sin(F0))
dX_dF1 = R*np.cos(np.radians(lon1 - lon0)*np.sin(np.radians(lat0)))
dX_dF2 = R*np.cos(np.radians(lon2 - lon0)*np.sin(np.radians(lat0)))
# dY_dF=-R*sin((L - L0)*sin(F0))
dY_dF1 = -R*np.sin(np.radians(lon1 - lon0)*np.sin(np.radians(lat0)))
dY_dF2 = -R*np.sin(np.radians(lon2 - lon0)*np.sin(np.radians(lat0)))
# dX_dl=R*(-F + F0 + cot(F0))*sin(F0)*sin((L - L0)*sin(F0))
dX_dl1 = R*(-np.radians(lat1) + np.radians(lat0) + 1/np.tan(np.radians(lat0)))*np.sin(np.radians(lat0))*np.cos(np.radians(lon1 - lon0)*np.sin(np.radians(lat0)))
dX_dl2 = R*(-np.radians(lat2) + np.radians(lat0) + 1/np.tan(np.radians(lat0)))*np.sin(np.radians(lat0))*np.cos(np.radians(lon2 - lon0)*np.sin(np.radians(lat0)))
# dY_dl=R*(-F + F0 + cot(F0))*sin(F0)*cos((L - L0)*sin(F0))
dY_dl1 = -(-np.radians(lat1) + np.radians(lat0) + 1/np.tan(np.radians(lat0)))*np.sin(np.radians(lat0))*np.sin(np.radians(lon1 - lon0)*np.sin(np.radians(lat0)))
dY_dl2 = -(-np.radians(lat2) + np.radians(lat0) + 1/np.tan(np.radians(lat0)))*np.sin(np.radians(lat0))*np.sin(np.radians(lon2 - lon0)*np.sin(np.radians(lat0)))

# tan(gamma) = dX_dF/dY_dF
gamma1 = np.degrees(np.arctan2(dX_dF1, dY_dF1))
gamma2 = np.degrees(np.arctan2(dX_dF2, dY_dF2))
print(f"5.1 Convergence of meridians: {gamma1:.2f} deg, {gamma2:.2f} deg")

E = R**2
G = R**2*np.cos(np.radians(lat0))**2

# dX_dl=R*(-F + F0 + cot(F0))*sin(F0)*sin((L - L0)*sin(F0))
dX_dl1 = R*(-np.radians(lat1) + np.radians(lat0) + 1/np.tan(np.radians(lat0)))*np.sin(np.radians(lat0))*np.cos(np.radians(lon1 - lon0)*np.sin(np.radians(lat0)))
dX_dl2 = R*(-np.radians(lat2) + np.radians(lat0) + 1/np.tan(np.radians(lat0)))*np.sin(np.radians(lat0))*np.cos(np.radians(lon2 - lon0)*np.sin(np.radians(lat0)))
# dY_dl=R*(-F + F0 + cot(F0))*sin(F0)*cos((L - L0)*sin(F0))
dY_dl1 = R*(-np.radians(lat1) + np.radians(lat0) + 1/np.tan(np.radians(lat0)))*np.sin(np.radians(lat0))*np.cos(np.radians(lon1 - lon0)*np.sin(np.radians(lat0)))
dY_dl2 = R*(-np.radians(lat2) + np.radians(lat0) + 1/np.tan(np.radians(lat0)))*np.sin(np.radians(lat0))*np.cos(np.radians(lon2 - lon0)*np.sin(np.radians(lat0)))

# E' = dX_dF1*dY_dl1 - dX_dl1*dY_dF1
E1 = dX_dF1*dY_dl1 - dX_dl1*dY_dF1
E2 = dX_dF2*dY_dl2 - dX_dl2*dY_dF2
# F' = dX_dF1*dX_dl1 + dY_dF1*dY_dl1
F1 = dX_dF1*dX_dl1 + dY_dF1*dY_dl1
F2 = dX_dF2*dX_dl2 + dY_dF2*dY_dl2
# Q = F'/sqrt(E*G)
Q1 = F1/np.sqrt(E*G)
Q2 = F2/np.sqrt(E*G)
# P = E'/E
P1 = E1/E
P2 = E2/E
# tan(A') = p*sin(A)/P*cos(A) + Q*sin(A)
A12p = np.degrees(np.arctan2(P1*np.sin(np.radians(A12T)), P1*np.cos(np.radians(A12T)) + Q1))
A21p = np.degrees(np.arctan2(P2*np.sin(np.radians(A21T)), P2*np.cos(np.radians(A21T)) + Q2))
print(f"5.2 Topographic azimuths: A12T: {abs(A12p):.2f} deg, A21T: {abs(A21p):.2f} deg")
delta12 = A12T - gamma1 - A12p
delta21 = A21T - gamma2 - A21p
print(f"5.3 Reduction angles: {delta12:.2f} deg, {delta21:.2f} deg")


# plot the points
import matplotlib.pyplot as plt
# set equal axis
plt.axis("equal")
plt.plot([x1, x2], [y1, y2], "ro-")
plt.text(x1, y1, name1)
plt.text(x2, y2, name2)
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title("Innsbruck and Vienna on the plane")
plt.grid()
plt.show()


"""
Ćwiczenie 3
Obliczenie redukcji odwzorowawczych oraz zniekształceń skończonych
Ćwiczenie polega na wykonaniu obliczeń redukcji i zniekształceń odwzorowawczych
długości odcinka linii łączącej punkty z ćwiczenia 1 w odwzorowaniu z ćwiczenia 2.
Dane do ćwiczenia 3 bierzemy z ćwiczenia 1 tzn. współrzędne geograficzne dwóch
punktów, które wybraliśmy na mapie obszaru. Następnie wykonujemy obliczenia długości
odcinka linii koła wielkiego łączącej te dwa punkty, azymutów tej linii, długości
odpowiednika redukcyjnego tej linii oraz dwiema metodami długość obrazu tej linii w
odwzorowaniu z ćwiczenia 2. Następnie obliczamy kąty redukcyjne oraz redukcje długości
oraz zniekształcenia długości.
Ćwiczenie powinno być oddane w formie sprawozdania pisemnego zawierającego
następujące elementy:
1. Tytuł:
Obliczenie redukcji odwzorowawczych oraz zniekształceń skończonych
2. Imię nazwisko studenta
3. Funkcje odwzorowawcze w zadanym odwzorowaniu (z ćwiczenia 2)
4. Dane do wykonania ćwiczenia (z ćwiczenia 1):
4.1.Nazwy miejscowości
4.2 Współrzędne geograficzne tych miejscowości, tj. dane do wykonania ćwiczenia
tzn. współrzędne geograficzne wybranych dwóch punktów P1 i P2=1

...=1

...=2

...=2

...
5 Wyniki obliczeń:
Długość odcinka P1P2 (w metrach) na powierzchni oryginału
d12=...
5.1 Azymuty linii P12, czyli A12 i A21 (w stopniach).
A12=...
A21=...
5.2 Współrzędne prostokątne obrazów punktów P1 i P2 czyli P1’(x1,y1) i P2’(x2,y2).
x1=...
y1=...
x2=...
y2=…
5.3 Długość odpowiednika redukcyjnego linii P1P2 czyli d12” (w metrach)
d12”=...
5.4 Azymuty topograficzne odpowiednika redukcyjnego, czyli AT12, AT21 (w
stopniach)
AT12=...
AT21=...
5.5 Zbieżności południków w punktach P1’ i P2’(w stopniach)...12 =
...21 =

5.6 Kąty redukcyjne (w stopniach)
...12 =
...21 =
5.7 Długość obrazu linii P1P2 obliczona dwukrotnie:
5.7.1 Jako aproksymacja łukiem okręgu
d12’1=...
5.7.2 Za pomocą skal zniekształceń długości
d12’2=...
5.8 Redukcje długości linii P1P2 obliczone jako różnice i ilorazy
d12”/d12=...
d12”-d12=...
5.9 Zniekształcenia skończone długości linii P1P2 obliczone dwukrotnie jako różnice i
ilorazy
d12’1/d12=...
d12’2/d12=...
d12’1-d12=...
d12’2=d12=...
Wyjaśnienie ćwiczenia
Etapy obliczania redukcji odwzorowawczych dla odcinka P1P2:
1. Wybieramy dwa punkty (miejscowości z ćwiczenia 1)
P1(1,1) oraz P2(2,2)
Na powierzchni oryginału (sferze) mamy dany odcinek linii koła wielkiego jak na rys. 1.
Rysunek 1.
2. Wyznaczamy długość linii P1P2 na sferze, w tym celu stosujemy wzory
trygonometrii sferycznej:)12cos()22/sin()12/sin()22/cos()12/cos(])[12cos(










−−−+−−=radd
d12[m]=R*d12[rad], gdzie R=6371000m
Obliczamy długość tego odcinka i azymuty. Rozwiązując trójkąt sferyczny jak na rys. 2.
Rysunek 2.
3. Wyznaczamy azymuty geograficzne A12 oraz A21 (również stosujemy wzory
trygonometrii sferycznej):
L12=sin(2)cos(1)- cos(2)sin(1)cos(2-1)
M12=cos(2)sin((2-1)
tan(A12)=L12/M12
L21=sin(1)cos(2)- cos(1)sin(2)cos(1-2)
M21=cos(1)sin((2-1)
tan(A21)=L21/M21
4. Obliczenie odpowiednika redukcyjnego linii P1P2
4.1 Obliczamy współrzędne prostokątne płaskie obrazów punktów P1 i P2 w
odwzorowaniu z ćwiczenia 2:
P1’(X1,Y1), P2’(X2,Y2)
Na płaszczyźnie mamy obraz odcinka P1P2 (na rys.3 kolor niebieski) i odpowiednik
redukcyjny tego odcinka (czerwony) jak na rys. 3. Obliczamy najpierw długość i azymuty
odcinka prostej.
Rysunek 3.
4.2 Obliczamy długość odcinka prostej P1’P2’:( ) ( )
22 1212"12 YYXXd −+−=
4.3 Obliczamy redukcje długości: d12-d12”
4.4 Obliczamy azymuty topograficzne A12T, A21T:12
12
12tan XX
YY
TA −
−
=
,21
21
21tan XX
YY
TA −
−
=
5. Wyznaczenie obrazu linii P1P2
Obliczamy długość obrazu linii P1P2 (na rys. 3 na niebiesko) dwiema metodami.
5.1 Obliczamy zbieżności południków w punktach P1’ oraz P2’:


d
dy
d
dx
=tan
,
w tym celu korzystamy z pochodnych cząstkowych funkcji odwzorowawczych
policzonych względem szerokości geograficznej. Obliczamy najpierw te pochodne w obu
punktach:1
1





=
=






d
dx
,1
1





=
=






d
dy oraz2
2





=
=






d
dx ,2
2





=
=






d
dy
a następnie zbieżności południków1
1
1
1
1tan











=
=
=
=












=
d
dy
d
dx
,2
2
2
2
2tan











=
=
=
=












=
d
dy
d
dx
UWAGA: w odwzorowaniach walcowych zbieżność południków jest równa 0. W
odwzorowaniach azymutalnych zbieżność południków jest równa długości geograficznej
w danym punkcie. W odwzorowaniach stożkowych jest równa długości geograficznej
pomnożonej przez stałą c.
5.2 Obliczamy obrazy azymutów geograficznych A12’ i A21’ ze wzoru:
AQAP
Ap
A sincos
sin
'tan +
=gdzie p- skala zniekształceń pól,E
E
P '
= ,EG
F
Q '
=
UWAGA: w odwzorowaniach walcowych, azymutalnych i stożkowych Q=0. W
odwzorowaniach równopolowych p=1; W odwzorowaniach równokątnych A’=A.
5.3 Obliczamy kąty redukcyjne:'1211212 ATA −−=

 oraz'2122121 ATA −−=


5.4 Obliczamy długości d12’ odpowiedników obrazowych boków trójkąta
aproksymowanych łukami okręgów, zgodnie z rysunkiem 4
Rysunek 4.
Długość łuku łączącego punkty'1P i'2P :xrd ='12
gdzie
2=x)90cos(
"5.0 12

−
= d
r2
2112



+
=
Długości odpowiedników obrazowych obliczamy drugi raz, tym razem na podstawie skal
zniekształceń długości. W punktach'1P i'2P obliczamy skale długości  oraz  dla
azymutów A12 i A21:ARAQAP 22 sin2sincos ++=

gdzieE
E
P '
= ,EG
F
Q '
= ,G
G
R '
=
a potem średnią:
2
2112



+
=śra następnie długość odpowiednika obrazowego:12'12 dd śr

=
Przykład
W przykładzie obliczenia przeprowadzono w programie OCTAVE, dla odwzorowania
azymutalnego równopolowego Lamberta:




 −




 −=−




 −−== )sin(
24
sin2),cos(
24
sin2' 00








RyRxr

.
Dane są dwa punkty o współrzędnych geograficznych:( )
 14,48 111 ==


P
,( )
 25,54 222 ==


P
Przyjmiemy, że
190 =
 .
Obliczamy pochodne cząstkowe funkcji odwzorowawczych:




 −




 −−=−




 −== )sin(
24
cos),cos(
24
cos' 00









R
d
dy
R
d
dx
r





 −




 −=−




 −== )cos(
24
sin2),sin(
24
sin2' 00









R
d
dy
R
d
dx
r

W pierwszej kolejności policzymy długość na sferze d12 i azymuty A12 oraz A21:
Obliczając azymuty korzystamy z funkcji atan2.
Wyniki są następujące:
Następnie obliczamy współrzędne prostokątne X1,Y1,X2,Y2 punktów P1’ i P2’ oraz długość
prostej d12” i azymuty topograficzne A12” i A21”:
Wyniki są następujące:
Następnie obliczamy skalę zniekształceń długości w punkcie P1 dla azymutu A12:
Wyniki są następujące:
Następnie obliczamy skalę zniekształceń długości w punkcie P2 dla azymutu A21:
Wyniki są następujące:
Obliczamy średnią wartość skali misr oraz przybliżoną długość odpowiednika obrazowego
d12’:
wyniki:
Obliczenie zbieżności południków, obrazów azymutów, kątów redukcyjnych oraz długości
obrazu linii geodezyjnej.
wyniki:
Obliczenie redukcji i zniekształceń długości:
wyniki obliczenia redukcji i zniekształceń:
Redukcja długości odcinka wynosi 11.054 km, zniekształcenie to ok. 11 km. Zniekształcenie
obliczone za pomocą aproksymacji łukiem okręgu wyszło 11.228 km a za pomocą skal
zniekształceń 10.926km, Obie wartości są jedynie przybliżeniem.
"""


