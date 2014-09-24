
function calcspec = fSambuca(CHL,CDOM,TR,q,H,UQSubs, filtsum,wav, awater, aphy_star,d_wls,n_wls,filt)

% SIOP and image acquistion parameters
% ***************************************************
X_ph_lambda0x = 0.00157747;
X_tr_lambda0x = 0.0225353;
Sc = 0.0168052;
Str = 0.00977262;
a_tr_lambda0tr = 0.00433;
Y = 0.878138;
Qwater = 4.00;
lambda0cdom=550.00;
a_cdom_lambda0cdom = 1.0;
PI=3.14159265;
theta_air=30; %solar zenith
offnad=10; % off nadir angle

%SUBS
r1=UQSubs(:,1);
r2=UQSubs(:,2);

% Semi analytical Lee/Sambuca forward model
% ************************************************************************

thetaw = (asin(1/1.333*sin(PI/180.00*(theta_air))));
thetao = (asin(1/1.333*sin(PI/180.00*(offnad))));

for i=1:d_wls
bbwater(i)= ( 0.00194/2.0 ) * ( ( 550.0/wav(i) )^4.32 );
acdom_star(i) = a_cdom_lambda0cdom * (exp(-Sc * (wav(i) - 550.00) ) );
atr_star(i) = a_tr_lambda0tr * (exp(-Str * (wav(i) - 550.00) ) ); 
bbph_star(i) = X_ph_lambda0x * ( (546.00/wav(i))^Y );
bbtr_star(i) = X_tr_lambda0x * ( (546.00/wav(i))^Y );
end

for i=1:d_wls
a(i) = awater(i) +  (CHL * aphy_star(i)) + (CDOM  * acdom_star(i)) + (TR * atr_star(i));
bb(i) =  bbwater(i) + (CHL * bbph_star(i)) + (TR * bbtr_star(i));
end


for i=1:d_wls
r(i) = (q * r1(i)) + ( (1-q) * r2(i) ); % substrate spectra - Will need modification for more then two spectra
u(i) = bb(i) / (a(i) + bb(i));
kappa(i) = a(i) + bb(i);
end


for i=1:d_wls
DuColumn(i) = 1.03 * (1.00 + (2.40 * u(i)) )^0.50; 
DuBottom(i) = 1.04 * (1.00 + (5.40 * u(i)) )^0.50;
end

for i=1:d_wls
rrsdp(i) = (0.084 + (0.17 * u(i)) ) * u(i) ;
Kd(i)=   kappa(i) * (1.00     / cos(thetaw)); 
Kuc(i)=  kappa(i) * (DuColumn(i) / cos(thetao));
Kub(i)=  kappa(i) * (DuBottom(i) / cos(thetao));
end

for i=1:d_wls
rrs(i) = rrsdp(i) * (1.00 - exp(-( (1.00/cos(thetaw)) + (DuColumn(i) / cos(thetao)) )* kappa(i) * H)) + ( (1.00/PI) * r(i) * exp(-( (1.00/cos(thetaw)) + (DuBottom(i) / cos(thetao)) )* kappa(i) * H)   );
end

bandsum(1:36)=0;
 calc(1:551,1:36) = 0;

for j=1:n_wls
	for i=1:d_wls
		calc(i,j) = rrsdp(i) * filt(i,j);
		bandsum(j) = bandsum(j)+ calc(i,j);
    end
end

for i=1:n_wls
 calcspec(i) = bandsum(i)/filtsum(i);
end


