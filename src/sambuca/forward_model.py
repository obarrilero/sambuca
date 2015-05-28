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
        qwater=1.0,
        x_ph_lambda0x=0.00157747,
        x_tr_lambda0x=0.0225353,
        sc=0.0168052,
        str_=0.00977262,
        a_tr_lambda0tr=0.00433,
        y=0.878138,
        lambda0cdom=550.0,
        lambda0tr=550.0,
        lambda0x=546.0,
        a_cdom_lambda0cdom=1.0,
        theta_air=30.0,
        off_nadir=0.0):
    """Semi analytical Lee/Sambuca forward model.

    TODO: Extended description goes here.
    TODO: For those arguments which have units, the units should be stated.
    TODO: should qwater have a default value? If so, what should it be?

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
        qwater (float): TODO
        x_ph_lambda0x (float, optional): specific backscatter of chlorophyl
            at lambda0x.
        x_tr_lambda0x (float, optional): specific backscatter of tripton
            at lambda0x.
        sc (float, optional): slope of cdom absorption
        str_ (float, optional): slope of NAP/tripton absorption
        a_tr_lambda0tr (float, optional): TODO
        y (float, optional): TODO
        lambda0cdom (float, optional): TODO
        lambda0tr (float, optional): TODO
        lambda0x (float, optional): TODO
        a_cdom_lambda0cdom (float, optional):
        theta_air (float, optional): solar zenith angle in degrees
        off_nadir (float, optional): off-nadir angle

    Returns:
        Dictionary: A dictionary containing the model outputs.

        TODO: Will it be faster to only calculate requested outputs from a set?

        - **substrate_r** (*ndarray*): The combined substrate.
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

    # Sub-surface solar zenith angle in radians
    # TODO: better name for this value
    solar_constant = 1.0 / 1.333
    thetaw = math.asin(solar_constant * math.sin(math.radians(theta_air)))

    # Sub-surface viewing angle in radians
    # TODO: Reconcile thetao calculation difference between IDL and Matlab
    thetao = math.asin(solar_constant * math.sin(math.radians(off_nadir)))
    # thetao = 0.0

    # Calculate derived SIOPS
    # TODO: In the IDL code, these are calculated just once for a pixel.
    # TODO: should this be lambda0cdom, or hardcoded 550?
    # bbwater = (0.00194 / 2.0) * np.power(lambda0cdom / wav, 4.32)
    bbwater = (0.00194 / 2.0) * np.power(550.0 / wav, 4.32)  # Mobely, 1994
    acdom_star = a_cdom_lambda0cdom * np.exp(-sc * (wav - lambda0cdom))
    atr_star = a_tr_lambda0tr * np.exp(-str_ * (wav - lambda0tr))

    # Calculate backscatter
    backscatter = np.power(lambda0x / wav, y)
    # backscatter due to phytoplankton
    bbph_star = x_ph_lambda0x * backscatter
    # backscatter due to tripton
    bbtr_star = x_tr_lambda0x * backscatter

    # TODO: what do a and bb represent? absorption and backscatter?
    a = awater + chl * aphy_star + cdom * acdom_star + nap * atr_star
    bb = bbwater + chl * bbph_star + nap * bbtr_star

    # Calculate total bottom reflectance from the two substrates and the
    # substrate interpolation factor q
    r = q * substrate1 + (1. - q) * substrate2

    # TODO: what are u and kappa?
    u = bb / (a + bb)
    kappa = a + bb

    # Optical path elongation for scattered photons
    # elongation from water column
    du_column = 1.03 * np.power(1.00 + (2.40 * u), 0.50)
    # elongation from bottom
    du_bottom = 1.04 * np.power(1.00 + (5.40 * u), 0.50)

    # Remotely sensed reflectance for optically deep water
    rrsdp = (0.084 + 0.17 * u) * u

    inv_cos_thetaw = 1.0 / math.cos(thetaw)

    # TODO: descriptions of kd, kuc, kub
    kd = kappa * inv_cos_thetaw
    kuc = kappa * (du_column / math.cos(thetao))
    kub = kappa * (du_bottom / math.cos(thetao))

    # Remotely sensed reflectance
    du_column_scaled = du_column / math.cos(thetao)
    du_bottom_scaled = du_bottom / math.cos(thetao)
    kappa_h = kappa * h
    rrs = (rrsdp *
           (1. - np.exp(-(inv_cos_thetaw + du_column_scaled) * kappa_h)) +
           ((1. / math.pi) * r *
            np.exp(-(inv_cos_thetaw + du_bottom_scaled) * kappa_h)))

    # Closed spectra
    closed_spectrum = rrs * qwater
    closed_deep_spectrum = rrsdp * qwater

    # TODO: generate and fill in all results
    results = {
        'substrate_r': r,
        'closed_spectrum': closed_spectrum,
        'closed_deep_spectrum': closed_deep_spectrum,
        'kd': kd,
        'kuc': kuc,
        'kub': kub,
    }
    return results

# pylint: enable=too-many-arguments
# pylint: enable=invalid-name
# pylint: enable=too-many-locals
