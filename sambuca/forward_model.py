"""Semi-analytical Lee/Sambuca forward model.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import math

import numpy as np

from .constants import REFRACTIVE_INDEX_SEAWATER


# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

# Disabling invalid-name as many of the common (and published) variable names
# in the Sambuca model are invalid according to Python conventions.
# pylint: disable=invalid-name
def forward_model(
        chl,
        cdom,
        nap,
        depth,
        substrate_fraction,
        substrate1,
        substrate2,
        wav,
        awater,
        aphy_star,
        num_bands,
        slope_cdom=0.0168052,
        slope_nap=0.00977262,
        slope_backscatter=0.878138,
        lambda0cdom=550.0,
        lambda0tr=550.0,
        lambda0x=546.0,
        x_ph_lambda0x=0.00157747,
        x_tr_lambda0x=0.0225353,
        a_cdom_lambda0cdom=1.0,
        a_tr_lambda0tr=0.00433,
        bb_lambda_ref=550,
        water_refractive_index=REFRACTIVE_INDEX_SEAWATER,
        theta_air=30.0,
        off_nadir=0.0):
    """Semi-analytical Lee/Sambuca forward model.

    TODO: Extended description goes here.

    TODO: For those arguments which have units, the units should be stated.

    Args:
        chl (float): Concentration of chlorophyll (algal organic particles).
        cdom (float): Concentration of coloured dissolved organic particulates.
        nap (float): Concentration of non-algal particles,
            (also known as Tripton/tr in some literature).
        depth (float): Water column depth.
        substrate_fraction (float): Substrate proportion, used to generate a
            convex combination of substrate1 and substrate2.
        substrate1 (array-like): A benthic substrate.
        substrate2 (array-like): A benthic substrate.
        wav (array-like): TODO
        awater (array-like): Absorption coefficient of pure water
        aphy_star (array-like): Specific absorption of phytoplankton.
        num_bands (int): The number of spectral bands.
        slope_cdom (float, optional): slope of cdom absorption
        slope_nap (float, optional): slope of NAP absorption
        slope_backscatter (float, optional): TODO
        lambda0cdom (float, optional): TODO
        lambda0tr (float, optional): TODO
        lambda0x (float, optional): TODO
        x_ph_lambda0x (float, optional): specific backscatter of chlorophyl
            at lambda0x.
        x_tr_lambda0x (float, optional): specific backscatter of tripton
            at lambda0x.
        a_cdom_lambda0cdom (float, optional): TODO
        a_tr_lambda0tr (float, optional): TODO
        bb_lambda_ref (float, optional): TODO
        water_refractive_index (float, optional): refractive index of water.
        theta_air (float, optional): solar zenith angle in degrees
        off_nadir (float, optional): off-nadir angle

    Returns:
        Dictionary: A dictionary containing the model outputs.

        TODO: Will it be faster to only calculate requested outputs from a set?

        - **substrate_r** (*ndarray*): The combined substrate.
        - **rrs** (*ndarray*): Modelled remotely-sensed reflectance.
        - **rrsdp** (*ndarray*): Modelled optically-deep
            remotely-sensed reflectance.
        - **kd** (*ndarray*): TODO
        - **kuc** (*ndarray*): TODO
        - **kub** (*ndarray*): TODO
        - **a** (*ndarray*): TODO
        - **bb** (*ndarray*): TODO


    """

    assert len(substrate1) == num_bands
    assert len(substrate2) == num_bands
    assert len(wav) == num_bands
    assert len(awater) == num_bands
    assert len(aphy_star) == num_bands

    # Sub-surface solar zenith angle in radians
    inv_refractive_index = 1.0 / water_refractive_index
    thetaw = math.asin(inv_refractive_index * math.sin(math.radians(theta_air)))

    # Sub-surface viewing angle in radians
    thetao = math.asin(inv_refractive_index * math.sin(math.radians(off_nadir)))

    # Calculate derived SIOPS, based on
    # Mobley, Curtis D., 1994: Radiative Transfer in natural waters.
    bbwater = (0.00194 / 2.0) * np.power(bb_lambda_ref / wav, 4.32)
    acdom_star = a_cdom_lambda0cdom * np.exp(-slope_cdom * (wav - lambda0cdom))
    atr_star = a_tr_lambda0tr * np.exp(-slope_nap * (wav - lambda0tr))

    # Calculate backscatter
    backscatter = np.power(lambda0x / wav, slope_backscatter)
    # backscatter due to phytoplankton
    bbph_star = x_ph_lambda0x * backscatter
    # backscatter due to tripton
    bbtr_star = x_tr_lambda0x * backscatter

    # Total absorption
    a = awater + chl * aphy_star + cdom * acdom_star + nap * atr_star
    # Total backscatter
    bb = bbwater + chl * bbph_star + nap * bbtr_star

    # Calculate total bottom reflectance from the two substrates
    r_substratum = substrate_fraction * substrate1 + \
        (1. - substrate_fraction) * substrate2

    # TODO: what are u and kappa?
    kappa = a + bb
    u = bb / kappa

    # Optical path elongation for scattered photons
    # elongation from water column
    # TODO: reference to the paper from which these equations are derived
    du_column = 1.03 * np.power(1.00 + (2.40 * u), 0.50)
    # elongation from bottom
    du_bottom = 1.04 * np.power(1.00 + (5.40 * u), 0.50)

    # Remotely sensed reflectance for optically deep water
    rrsdp = (0.084 + 0.17 * u) * u

    # common terms in the following calculations
    inv_cos_thetaw = 1.0 / math.cos(thetaw)
    inv_cos_theta0 = 1.0 / math.cos(thetao)
    du_column_scaled = du_column * inv_cos_theta0
    du_bottom_scaled = du_bottom * inv_cos_theta0

    # TODO: descriptions of kd, kuc, kub
    kd = kappa * inv_cos_thetaw
    kuc = kappa * du_column_scaled
    kub = kappa * du_bottom_scaled

    # Remotely sensed reflectance
    kappa_d = kappa * depth
    rrs = (rrsdp *
           (1.0 - np.exp(-(inv_cos_thetaw + du_column_scaled) * kappa_d)) +
           ((1.0 / math.pi) * r_substratum *
            np.exp(-(inv_cos_thetaw + du_bottom_scaled) * kappa_d)))

    results = {
        'substrate_r': r_substratum,
        'rrs': rrs,
        'rrsdp': rrsdp,
        'kd': kd,
        'kuc': kuc,
        'kub': kub,
        'a': a,
        'bb': bb,
    }
    return results

# pylint: enable=too-many-arguments
# pylint: enable=invalid-name
# pylint: enable=too-many-locals
