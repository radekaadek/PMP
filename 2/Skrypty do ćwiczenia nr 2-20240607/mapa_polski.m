clear all;
R=6371;
L0=19*pi/180;
%generowanie macierzy punktow wezlowych siatki
no_f=8;
no_l=12;
f=linspace(48*pi/180,55*pi/180,no_f);
l=linspace(14*pi/180,25*pi/180,no_l);
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
delta_f=1;
for i=1:delta_f:no_f;
    plot(Y(i,:),X(i,:),'r');
end

delta_l=1;
for i=1:delta_l:no_l;
    plot(Y(:,i),X(:,i),'r');
end

%odczytywanie wspolrzednych (fi,lambda) kontynent�w
fid = fopen('brzegpol.txt','r');
[A,inf] = fscanf(fid,'%f %f',[2 inf]);
Fk=(A(1,:))*pi/180;
Lk=(A(2,:))*pi/180;

%wzor na odwzorowanie
Xk=R*Fk;
Yk=R*cos(Fk).*(Lk-L0);

%wrysowanie konturu Polski
plot(Yk,Xk);
