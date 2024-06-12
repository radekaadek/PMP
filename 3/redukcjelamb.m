

R=6371;

% lat1, lon1 = 47.280407, 11.409991 # Innsbruck
% lat2, lon2 = 48.201961, 16.3646931 # Vienna
% lat0, lon0 = lat1+lat2/2, lon1+lon2/2
fi1=47.280407*pi/180;
lam1=11.409991*pi/180;
fi2=48.201961*pi/180;
lam2=16.3646931*pi/180;
fi0=(fi1+fi2)/2;
lam0=(lam1+lam2)/2;


cd12=cos(pi/2-fi1)*cos(pi/2-fi2)+sin(pi/2-fi1)*sin(pi/2-fi2)*cos(lam2-lam1);
d12=R*acos(cd12);

printf("d12 %f\n", d12);


M12=sin(fi2)*cos(fi1)-cos(fi2)*sin(fi1)*cos(lam2-lam1);
L12=cos(fi2)*sin(lam2-lam1);
A12=atan2(L12,M12);
A12st=180*atan2(L12,M12)/pi;

printf("A12st %f\n", A12st);

M21=sin(fi1)*cos(fi2)-cos(fi1)*sin(fi2)*cos(lam1-lam2)
L21=cos(fi1)*sin(lam1-lam2);
A21=atan2(L21,M21)
A21st=180*atan2(L21,M21)/pi;

printf("A21st %f\n",A21st);
sin_fi0 = sin(fi0);
X1=-R * (cot(fi0) + fi0 - fi1) .* cos(sin_fi0 * (lam1 - lam0));
Y1=R * (cot(fi0) + fi0 - fi1) .* sin(sin_fi0 * (lam1 - lam0));
X2=-R * (cot(fi0) + fi0 - fi2) .* cos(sin_fi0 * (lam2 - lam0));
Y2=R * (cot(fi0) + fi0 - fi2) .* sin(sin_fi0 * (lam2 - lam0));

printf("  X1= %f\n  Y1= %f\n  X2= %f\n  Y2= %f\n",X1,Y1,X2,Y2);

d12bis=sqrt((X2-X1)^2+(Y2-Y1)^2);

printf("  d12bis %f\n", d12bis);

AT12=atan2(Y2-Y1,X2-X1);
AT12st=AT12*180/pi;
AT21=atan2(Y1-Y2,X1-X2);
AT21st=AT21*180/pi;

printf("  AT12st %f\n AT21st %f\n",AT12st,AT21st);

x_fi1=R*cos((lam1-lam0)*sin(fi0));
y_fi1=-R*sin((lam1-lam0)*sin(fi0));
x_l1=R*(-fi1+fi0+cot(fi0)).*sin(fi0).*sin((lam1-lam0)*sin(fi0));
y_l1=R*(-fi1+fi0+cot(fi0)).*sin(fi0).*cos((lam1-lam0)*sin(fi0));

Ep1=x_fi1.^2+y_fi1.^2;;
Fp1=x_fi1.*x_l1+y_fi1.*y_l1;
Gp1=x_l1.^2+y_l1.^2;
Hp1=abs(x_fi1.*y_l1-y_fi1.*x_l1);
Pd1=Ep1./(R.^2);
Rd1=Gp1./(R.^2.*cos(fi1).^2);
p1=Hp1./(R.^2.*cos(fi1));
Qd1=Fp1./(R.^2.*cos(fi1));
mi12=sqrt(Pd1*cos(A12)^2+Qd1*sin(2*(A12))+Rd1*sin(A12)^2);

printf("  mi12= %f\n",mi12);

x_fi2=R*cos((lam2-lam0)*sin(fi0));
y_fi2=-R*sin((lam2-lam0)*sin(fi0));
x_l2=R*(-fi2+fi0+cot(fi0)).*sin(fi0).*sin((lam2-lam0)*sin(fi0));
y_l2=R*(-fi2+fi0+cot(fi0)).*sin(fi0).*cos((lam2-lam0)*sin(fi0));

Ep2=x_fi2.^2+y_fi2.^2;;
Fp2=x_fi2.*x_l2+y_fi2.*y_l2;
Gp2=x_l2.^2+y_l2.^2;
Hp2=abs(x_fi2.*y_l2-y_fi2.*x_l2);
Pd2=Ep2./(R.^2);
Rd2=Gp2./(R.^2.*cos(fi2).^2);
p2=Hp2./(R.^2.*cos(fi2));
Qd2=Fp2./(R.^2.*cos(fi2));
mi21=sqrt(Pd2*cos(A21)^2+Qd2*sin(2*(A21))+Rd2*sin(A21)^2);

printf("  mi12= %f\n",mi21);

misr=(mi12+mi21)/2;

printf("  misr= %f\n",misr);

d12pp=misr*d12;

printf("  d12pp= %f\n",d12pp);

gamma1=atan2(y_fi1,x_fi1);
gamma1st=gamma1*180/pi;

gamma2=atan2(y_fi2,x_fi2);
gamma2st=gamma2*180/pi;
printf("  gamma1= %f\n  gamma2= %f\n ",gamma1st,gamma2st);

A12p=atan2(p1*sin(A12),Pd1*cos(A12)+Qd1*sin(A12));
A12pst=A12p*180/pi;

A21p=atan2(p2*sin(A21),Pd2*cos(A21)+Qd2*sin(A21));
A21pst=A21p*180/pi;

printf("  A12pst= %f\n  A21pst= %f\n",A12pst,A21pst);

delta12=AT12-gamma1-A12p;
delta12st=delta12*180/pi;

delta21=AT21-gamma2-A21p;
delta21st=delta21*180/pi;

printf("  delta12st= %f\n  delta21st= %f\n",delta12st,delta21st);

delta=(abs(delta12)+abs(delta21))/2;

d12p=d12bis*delta/cos(pi/2-delta);

printf("  d12p= %f\n",d12p);

redroz=d12bis-d12;
redilor=d12bis/d12;
znroz1=d12p-d12;
znroz2=d12pp-d12;
znil1=d12p/d12;
znil2=d12pp/d12;

printf("  redroz= %f\n  redilor= %f\n  znroz1= %f\n znroz2= %f\n  znil1= %f\n  znil2= %f\n",redroz,redilor,znroz1,znroz2,znil1,znil2);
