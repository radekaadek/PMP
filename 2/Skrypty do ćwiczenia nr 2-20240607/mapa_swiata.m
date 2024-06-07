clear all;
R=6371000;
L0=0;
%generowanie macierzy punktow wezlowych siatki
no_f=181;
no_l=361;
f=linspace(-pi/2,pi/2,no_f);
l=linspace(-pi,pi,no_l);
[L,F] = meshgrid(l,f);

%wzor na odwzorowanie
% X=R*F;
% Y=R*cos(F).*(L-L0);
F0 = pi/2;
L0 = 0
cot_F0 = cot(F0);
sin_F0 = sin(F0);
ror = R*cot_F0 + R*F0;
c = sin(F0)
ro = ror - R*F;
delta = c*(L - L0);
X = -ro.*cos(delta);
Y = ro.*sin(delta);

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
fid = fopen('kontynenty.txt','r');
[A,inf] = fscanf(fid,'%f %f',[2 inf]);
Lk=(A(1,:))*pi/180;
Fk=(A(2,:))*pi/180;

%wzor na odwzorowanie
% Xk=R*Fk;
% Yk=R*cos(Fk).*(Lk-L0);
cot_F0 = cot(F0);
sin_F0 = sin(F0);
ror = R*cot_F0 + R*F0;
c = sin(F0)
ro = ror - R*Fk;
delta = c*(Lk - L0);
Xk = -ro.*cos(delta);
Yk = ro.*sin(delta);

%wrysowanie kontynentow
plot(Yk,Xk,'.','MarkerSize',4);
