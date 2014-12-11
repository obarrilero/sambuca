''' Implementation of the Sambuca forward model.
'''
import math
import numpy as np


# TODO: is the substrate loop inside or outside this function?
def forward_model(
        # pylint: disable=too-many-arguments
        # pylint: disable=invalid-name
        # pylint: disable=too-many-locals
        chl,
        cdom,
        tr,
        h,
        q,
        substrate1,
        substrate2,
        wav,
        awater,
        aphy_star,
        d_wls,
        x_ph_lambda0x=0.00157747,
        x_tr_lambda0x=0.0225353,
        sc=0.0168052,
        str_=0.00977262,
        a_tr_lambda0tr=0.00433,
        y=0.878138,
        lambda0cdom=550.00,
        a_cdom_lambda0cdom=1.0,
        theta_air=30,
        offnad=10):
    """Semi analytical Lee/Sambuca forward model.

    :param cdom: Model parameter. ...
    :param tr: Model parameter. ...
    :param h: Model parameter. ...
    :param q: Model parameter. ...
    :param substrate1:
    :param substrate2:
    :param wav:
    :param awater: SIOP...
    :param aphy_star: SIOP...
    :param d_wls: number of spectral bands
    :param x_ph_lambda0x:
    :param x_tr_lambda0x:
    :param sc:
    :param str_:
    :param a_tr_lambda0tr:
    :param y:
    :param lambda0cdom: Reference frequency?
    :param a_cdom_lambda0cdom:
    :param theta_air: solar zenith
    :param offnad: off-nadir angle
    """

    assert len(substrate1) == d_wls
    assert len(substrate2) == d_wls
    assert len(wav) == d_wls
    assert len(awater) == d_wls
    assert len(aphy_star) == d_wls

    thetaw = math.asin(1 / 1.333 * math.sin(math.pi / 180. * theta_air))
    thetao = math.asin(1 / 1.333 * math.sin(math.pi / 180. * offnad))

    # The wave lengths hardcoded here (550.00 and 546.00) are reference
    # wavelengths that are are actually part of the user defined SIOP set
    # TODO: 550 == lambda0cdom?
    # TODO: what is the name of the second reference frequency?
    # TODO: I think this direct port from Matlab is creating too many
    # intermediate arrays
    # TODO: some terms are reused and could be calculated just once
    bbwater = (0.00194/2.) * np.power(lambda0cdom / wav, 4.32)
    acdom_star = a_cdom_lambda0cdom * np.exp(-sc * (wav - lambda0cdom))
    atr_star = a_tr_lambda0tr * np.exp(-str_ * (wav - lambda0cdom))
    bbph_star = x_ph_lambda0x * np.power(546. / wav, y)
    bbtr_star = x_tr_lambda0x * np.power(546. / wav, y)
    # for i=1:d_wls
    # bbwater(i)= ( 0.00194/2.0 ) * ( ( 550.0/wav(i) )^4.32 );
    # acdom_star(i) = a_cdom_lambda0cdom * (exp(-Sc * (wav(i) - 550.00) ) );
    # atr_star(i) = a_tr_lambda0tr * (exp(-Str * (wav(i) - 550.00) ) );
    # bbph_star(i) = X_ph_lambda0x * ( (546.00/wav(i))^Y );
    # bbtr_star(i) = X_tr_lambda0x * ( (546.00/wav(i))^Y );
    # end

    a = awater + chl * aphy_star + cdom * acdom_star + tr * atr_star
    bb = bbwater + chl * bbph_star + tr * bbtr_star
    # for i=1:d_wls
    # a(i) = awater(i) + (CHL * aphy_star(i)) + (CDOM * acdom_star(i))
    #       + (TR * atr_star(i));
    # bb(i) =  bbwater(i) + (CHL * bbph_star(i)) + (TR * bbtr_star(i));
    # end

    # Calculates total bottom reflectance from the two substrates and the
    # proportion of q and (1-q)
    r = q * substrate1 + (1-q) * substrate2
    u = bb / (a + bb)
    kappa = a + bb
    # for i=1:d_wls
    # r(i) = (q * r1(i)) + ( (1-q) * r2(i) );
    # u(i) = bb(i) / (a(i) + bb(i));
    # kappa(i) = a(i) + bb(i);
    # end

    du_column = 1.03 * np.power(1.0 + (2.4 * u), 0.5)
    du_bottom = 1.04 * np.power(1.0 + (5.4 * u), 0.5)
    # for i=1:d_wls
    # DuColumn(i) = 1.03 * (1.00 + (2.40 * u(i)) )^0.50;
    # DuBottom(i) = 1.04 * (1.00 + (5.40 * u(i)) )^0.50;
    # end

    rrsdp = (0.084 + 0.17 * u) * u
    # TODO: Ask Steve why these are unused
    # kd = kappa * (1.0 / np.cos(thetaw))
    # kuc = kappa * (du_column / np.cos(thetao))
    # kub = kappa * (du_bottom / np.cos(thetao))
    # for i=1:d_wls
    # rrsdp(i) = (0.084 + (0.17 * u(i)) ) * u(i) ;
    # Kd(i)=   kappa(i) * (1.00     / cos(thetaw));
    # Kuc(i)=  kappa(i) * (DuColumn(i) / cos(thetao));
    # Kub(i)=  kappa(i) * (DuBottom(i) / cos(thetao));
    # end

    rrs = rrsdp * (1.0 - np.exp(-((1.0 / np.cos(thetaw)) + (du_column / np.cos(thetao))) * kappa * h)) \
        + ((1.0 / math.pi) * r * np.exp(-((1.0 / np.cos(thetaw)) + (du_bottom / np.cos(thetao))) * kappa * h))
    # for i=1:d_wls
    # rrs(i) = rrsdp(i) * (1.00 - exp(-( (1.00/cos(thetaw)) + (DuColumn(i) / cos(thetao)) )* kappa(i) * H)) + ( (1.00/PI) * r(i) * exp(-( (1.00/cos(thetaw)) + (DuBottom(i) / cos(thetao)) )* kappa(i) * H)   );
    # end

    return rrs
