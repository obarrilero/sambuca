""" Sambuca All Parameters

    Encapsulates all sambuca-core.forward_model arguments into a single
    namedtuple that is much easier to pass between various sambuca data
    structures.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

from collections import namedtuple

import numpy as np
import sambuca-core as sbc


AllParameters = namedtuple('AllParameters',
                            '''
                                chl,
                                cdom,
                                nap,
                                depth,
                                wavelengths,
                                a_water,
                                a_ph_star,
                                num_bands,
                                substrate_fraction,
                                substrate1,
                                substrate2,
                                a_cdom_slope,
                                a_nap_slope,
                                bb_ph_slope,
                                bb_nap_slope,
                                lambda0cdom,
                                lambda0nap,
                                lambda0x,
                                x_ph_lambda0x,
                                x_nap_lambda0x,
                                a_cdom_lambda0cdom,
                                a_nap_lambda0nap,
                                bb_lambda_ref,
                                water_refractive_index,
                                theta_air,
                                off_nadir,
                                q_factor
                            ''')
""" namedtuple containing all sambuca-core forward_model parameters.

Attributes:
        chl (float): Concentration of chlorophyll (algal organic particulates).
        cdom (float): Concentration of coloured dissolved organic particulates
            (CDOM).
        nap (float): Concentration of non-algal particulates (NAP).
        depth (float): Water column depth.
        substrate1 (array-like): A benthic substrate.
        wavelengths (array-like): Central wavelengths of the modelled
            spectral bands.
        a_water (array-like): Absorption coefficient of pure water
        a_ph_star (array-like): Specific absorption of phytoplankton.
        num_bands (int): The number of spectral bands.
        substrate_fraction (float): Substrate proportion, used to generate a
            convex combination of substrate1 and substrate2.
        substrate2 (array-like, optional): A benthic substrate.
        a_cdom_slope (float, optional): slope of CDOM absorption
        a_nap_slope (float, optional): slope of NAP absorption
        bb_ph_slope (float, optional): Power law exponent for the
            phytoplankton backscattering coefficient.
        bb_nap_slope (float, optional): Power law exponent for the
            NAP backscattering coefficient. If no value is supplied, the default
            behaviour is to use the bb_ph_slope value.
        lambda0cdom (float, optional): Reference wavelength for CDOM absorption.
        lambda0nap (float, optional): Reference wavelength for NAP absorption.
        lambda0x (float, optional): Backscattering reference wavelength.
        x_ph_lambda0x (float, optional): Specific backscatter of chlorophyl
            at lambda0x.
        x_nap_lambda0x (float, optional): Specific backscatter of NAP
            at lambda0x.
        a_cdom_lambda0cdom (float, optional): Absorption of CDOM at lambda0cdom.
        a_nap_lambda0nap (float, optional): Absorption of NAP at lambda0nap.
        bb_lambda_ref (float, optional): Reference wavelength for backscattering
            coefficient.
        water_refractive_index (float, optional): refractive index of water.
        theta_air (float, optional): solar zenith angle in degrees.
        off_nadir (float, optional): off-nadir angle.
        q_factor (float, optional): q value for producing the R(0-) values from
            modelled remotely-sensed reflectance (rrs) values.
"""


def create_fixed_parameter_set(
        wavelengths,
        a_water,
        a_ph_star,
        substrate1,
        substrate_fraction=1,
        substrate2=None,
        chl=None,
        cdom=None,
        nap=None,
        depth=None,
        a_cdom_slope=0.0168052,
        a_nap_slope=0.00977262,
        bb_ph_slope=0.878138,
        bb_nap_slope=None,
        lambda0cdom=550.0,
        lambda0nap=550.0,
        lambda0x=546.0,
        x_ph_lambda0x=0.00157747,
        x_nap_lambda0x=0.0225353,
        a_cdom_lambda0cdom=1.0,
        a_nap_lambda0nap=0.00433,
        bb_lambda_ref=550,
        water_refractive_index=sbc.REFRACTIVE_INDEX_SEAWATER,
        theta_air=30.0,
        off_nadir=0.0,
        q_factor=np.pi):
    """ Get an AllParameters tuple with Sambuca default values for use as
    a fixed parameter set.
    """

    return AllParameters(
        chl=chl,
        cdom=cdom,
        nap=nap,
        depth=depth,
        substrate_fraction=substrate_fraction,
        wavelengths=wavelengths,
        a_water=a_water,
        a_ph_star=a_ph_star,
        num_bands=len(wavelengths),
        substrate1=substrate1,
        substrate2=substrate2,
        a_cdom_slope=a_cdom_slope,
        a_nap_slope=a_nap_slope,
        bb_ph_slope=bb_ph_slope,
        bb_nap_slope=bb_nap_slope,
        lambda0cdom=lambda0cdom,
        lambda0nap=lambda0nap,
        lambda0x=lambda0x,
        x_ph_lambda0x=x_ph_lambda0x,
        x_nap_lambda0x=x_nap_lambda0x,
        a_cdom_lambda0cdom=a_cdom_lambda0cdom,
        a_nap_lambda0nap=a_nap_lambda0nap,
        bb_lambda_ref=bb_lambda_ref,
        water_refractive_index=water_refractive_index,
        theta_air=theta_air,
        off_nadir=off_nadir,
        q_factor=q_factor)
