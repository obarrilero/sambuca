"""Semi analytical Lee/Sambuca forward model.
"""

# Disable some pylint warnings caused by future and tkinter
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin

# Ensure compatibility of Python 2 with Python 3 constructs
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import math
import numpy as np


# pylint: disable=too-many-arguments
# pylint: disable=invalid-name
# pylint: disable=too-many-locals
def forward_model(
        chl,
        cdom,
        nap,
        h,
        q,
        substrate1,
        substrate2,
        wav,
        awater,
        aphy_star,
        num_bands,
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

    TODO: Extended description goes here.
    TODO: For those arguments which have units, the units should be stated.

    Args:
        chl (float): Concentration of chlorophyll (algal organic particles).
        cdom (float): Concentration of coloured dissolved organic particulates.
        nap (float): Concentration of non-algal particles,
            (also known as Tripton/tr in some literature).
        h (float): Depth.
        q (float): Substrate proportion, used to generate a convex combination
            of substrate1 and substrate2.
        substrate1 (array-like): A benthic substrate.
        substrate2 (array-like): A benthic substrate.
        wav (array-like): TODO
        awater (array-like): Absorption coefficient of pure water
        aphy_star (array-like): Specific absorption of phytoplankton.
        num_bands (int): The number of spectral bands.
        x_ph_lambda0x (float, optional): specific backscatter of chlorophyl
            at lambda0x.
        x_tr_lambda0x (float, optional): specific backscatter of tripton
            at lambda0x.
        sc (float, optional): slope of cdom absorption
        str_ (float, optional): slope of NAP/tripton absorption
        a_tr_lambda0tr (float, optional): TODO
        y (float, optional): TODO
        lambda0cdom (float, optional): Reference frequency?
        a_cdom_lambda0cdom (float, optional):
        theta_air (float, optional): solar zenith
        offnad (float, optional): off-nadir angle

    Returns:
        Dictionary: A dictionary containing the model outputs.

        TODO: Will it be faster to only calculate requested outputs from a set?

        - **substrateR** (*ndarray*): The combined substrate.
        - closed_spectrum (ndarray): Modelled remotely-sensed reflectance.
        - closed_deep_spectrum (ndarray): Modelled optically-deep
          remotely-sensed reflectance.
        - kd (ndarray): TODO
        - Kuc (ndarray): TODO
        - Kub (ndarray): TODO


    """

    assert len(substrate1) == num_bands
    assert len(substrate2) == num_bands
    assert len(wav) == num_bands
    assert len(awater) == num_bands
    assert len(aphy_star) == num_bands

    thetaw = math.asin(1 / 1.333 * math.sin(math.pi / 180. * theta_air))
    thetao = math.asin(1 / 1.333 * math.sin(math.pi / 180. * offnad))

    # The wave lengths hardcoded here (550.00 and 546.00) are reference
    # wavelengths that are are actually part of the user defined SIOP set
    # TODO: 550 == lambda0cdom?
    # TODO: what is the name of the second reference frequency?
    #   Arnold suggested it be made into an argument,
    #   but I don't know what to call it.
    bbwater = (0.00194/2.) * np.power(lambda0cdom / wav, 4.32)
    acdom_star = a_cdom_lambda0cdom * np.exp(-sc * (wav - lambda0cdom))
    atr_star = a_tr_lambda0tr * np.exp(-str_ * (wav - lambda0cdom))
    bbph_star = x_ph_lambda0x * np.power(546. / wav, y)
    bbtr_star = x_tr_lambda0x * np.power(546. / wav, y)

    a = awater + chl * aphy_star + cdom * acdom_star + nap * atr_star
    bb = bbwater + chl * bbph_star + nap * bbtr_star

    # Calculates total bottom reflectance from the two substrates and the
    # proportion of q and (1-q)
    r = q * substrate1 + (1. - q) * substrate2
    u = bb / (a + bb)
    kappa = a + bb

    du_column = 1.03 * np.power(1. + (2.4 * u), 0.5)
    du_bottom = 1.04 * np.power(1. + (5.4 * u), 0.5)

    # is this 'reflectance remotely sensed deep?'
    rrsdp = (0.084 + 0.17 * u) * u
    # kd = kappa * (1.0 / np.cos(thetaw))
    # kuc = kappa * (du_column / np.cos(thetao))
    # kub = kappa * (du_bottom / np.cos(thetao))

    inv_cos_thetaw = 1. / math.cos(thetaw)
    du_column_scaled = du_column / math.cos(thetao)
    du_bottom_scaled = du_bottom / math.cos(thetao)
    kappa_h = kappa * h
    rrs = (rrsdp *
           (1. - np.exp(-(inv_cos_thetaw + du_column_scaled) * kappa_h)) +
           ((1. / math.pi) * r *
            np.exp(-(inv_cos_thetaw + du_bottom_scaled) * kappa_h)))

    # TODO: generate and fill in all results
    results = {}
    return results
