sk=500; %skala elips
for i=1:delta_f:no_f;  
    for j=1:delta_l:no_l;
        mi1w=[x_fi;y_fi(i,j)]/R;
        mi2w=[x_l;y_l(i,j)]/(R*cos(F(i,j)));
        A=0;
        for v=1:180;
            mi=(mi1w*cos(A)+mi2w*sin(A));
            A=A+pi/90;
            wx(v)=X(i,j)+mi(1)*sk;
            wy(v)=Y(i,j)+mi(2)*sk;
        end;
       plot(wy,wx,'r');
    end;
end;
