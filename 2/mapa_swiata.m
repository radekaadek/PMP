clear all;
R=6371;
lat1 = 35;
lat2 = 75;
lon1 = -20;
lon2 = 45;
F0=(lat1+lat2)/2*pi/180;
L0=(lon1+lon2)/2*pi/180;
%generowanie macierzy punktow wezlowych siatki
no_f=181;
no_l=361;
f=linspace(lat1*pi/180,lat2*pi/180,no_f);
l=linspace(lon1*pi/180,lon2*pi/180,no_l);
[L,F] = meshgrid(l,f);

%wzor na odwzorowanie
% X=R*F;
% Y=R*cos(F).*(L-L0);

sin_F0 = sin(F0);
cot_F0 = cot(F0);
X = -R * (cot_F0 + F0 - F) .* cos(sin_F0 * (L - L0));
Y = R * (cot_F0 + F0 - F) .* sin(sin_F0 * (L - L0));

%parametry rysowania
figure(1);
axis equal;
hold on;

%rysowanie siatki
delta_f=15;
for i=1:delta_f:no_f;
    plot(Y(i,:),X(i,:),'b');
end
delta_l=30;
for i=1:delta_l:no_l;
    plot(Y(:,i),X(:,i),'b');
end

%odczytywanie wspolrzednych (fi,lambda) kontynent�w
fid = fopen('brzegpol.TXT','r');
[A,inf] = fscanf(fid,'%f %f',[2 inf]);
fclose(fid);
Lk=(A(1,:))*pi/180;
Fk=(A(2,:))*pi/180;
% filter out everything not in europe
Lk = Lk(Fk > lat1*pi/180 & Fk < lat2*pi/180);
Fk = Fk(Fk > lat1*pi/180 & Fk < lat2*pi/180);
Fk = Fk(Lk > lon1*pi/180 & Lk < lon2*pi/180);
Lk = Lk(Lk > lon1*pi/180 & Lk < lon2*pi/180);


%wzor na odwzorowanie
% Xk=R*Fk;
% Yk=R*cos(Fk).*(Lk-L0);
sin_F0 = sin(F0);
cot_F0 = cot(F0);
Xk = -R * (cot_F0 + F0 - Fk) .* cos(sin_F0 * (Lk - L0));
Yk = R * (cot_F0 + F0 - Fk) .* sin(sin_F0 * (Lk - L0));

%wrysowanie kontynentow
plot(Yk,Xk,'.','MarkerSize',4);
