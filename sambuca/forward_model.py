''' Implementation of the Sambuca forward model.
'''
import math
import numpy as np
import numexpr as ne


# TODO: is the substrate loop inside or outside this function?
def forward_model(
        # pylint: disable=too-many-arguments
        # pylint: disable=invalid-name
        # pylint: disable=too-many-locals
        # Squelch errors from the well-known issues that pylint has with numpy:
        # pylint: disable=no-member
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
    bbwater = ne.evaluate("(0.00194 / 2.) * ((lambda0cdom / wav) ** 4.32)")
    acdom_star = ne.evaluate("a_cdom_lambda0cdom * exp(-sc * (wav - lambda0cdom))")
    atr_star = ne.evaluate("a_tr_lambda0tr * exp(-str_ * (wav - lambda0cdom))")
    bbph_star = ne.evaluate("x_ph_lambda0x * ((546. / wav) ** y)")
    bbtr_star = ne.evaluate("x_tr_lambda0x * ((546. / wav) ** y)")
    a = ne.evaluate("awater + chl * aphy_star + cdom * acdom_star + tr * atr_star")
    bb = ne.evaluate("bbwater + chl * bbph_star + tr * bbtr_star")

    # Calculates total bottom reflectance from the two substrates and the
    # proportion of q and (1-q)
    r = ne.evaluate("q * substrate1 + (1. - q) * substrate2")
    u = ne.evaluate("bb / (a + bb)")
    kappa = ne.evaluate("a + bb")

    du_column = ne.evaluate("1.03 * ((1. + (2.4 * u)) ** 0.5)")
    du_bottom = ne.evaluate("1.04 * ((1. + (5.4 * u)) ** 0.5)")

    rrsdp = ne.evaluate("(0.084 + 0.17 * u) * u")
    # TODO: Ask Steve why these are unused
    # kd = kappa * (1.0 / np.cos(thetaw))
    # kuc = kappa * (du_column / np.cos(thetao))
    # kub = kappa * (du_bottom / np.cos(thetao))

    inv_cos_thetaw = 1. / math.cos(thetaw)
    du_column_scaled = ne.evaluate("du_column / cos(thetao)")
    du_bottom_scaled = ne.evaluate("du_bottom / cos(thetao)")
    kappa_h = ne.evaluate("kappa * h")
    pi = math.pi # required as numexpr does not understand pi or np.pi
    rrs = ne.evaluate("rrsdp * (1. - exp(-(inv_cos_thetaw + du_column_scaled) * kappa_h)) + ((1. / pi) * r * exp(-(inv_cos_thetaw + du_bottom_scaled) * kappa_h))")

    return rrs
