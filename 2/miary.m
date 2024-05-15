x_fi = R*cos((L - L0)*sin(F0))
y_fi = -R*sin((L - L0)*sin(F0))
x_l = R*(-F + F0 + cot(F0))*sin(F0)*sin((L - L0)*sin(F0))
y_l = R*(-F + F0 + cot(F0))*sin(F0)*cos((L - L0)*sin(F0))

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


