%Obliczenie miar zniekształceń odwzorowawczych
x_fi=R;
y_fi=-R*(L-L0).*sin(F);
x_l=0;
y_l=R*cos(F);

Ep=x_fi.^2+y_fi.^2;
Fp=x_fi.*x_l+y_fi.*y_l;
Gp=x_l.^2+y_l.^2;
Hp=abs(x_fi.*y_l-y_fi.*x_l);

Pd=Ep./(R.^2);
Rd=Gp./(R.^2.*cos(F).^2);

%skala pól
p=Hp./(R.^2.*cos(F));

A=sqrt(Pd+Rd+2*p);
B=sqrt(abs(Pd+Rd-2*p));
%skale ekstremalne
m=0.5*(A+B);
n=0.5*(A-B);


%zniekształcenia kątowe
zk=360*abs(atan((n-m)./(2*sqrt(p))))./pi;


