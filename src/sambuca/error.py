""" Sambuca Error Functions.

    Used when assessing model closure during parameter estimation.
"""
# Ensure compatibility of Python 2 with Python 3 constructs
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
# pylint: disable=no-member
from builtins import *

from collections import namedtuple
import numpy as np


def error_all(observed_rrs, modelled_rrs, nedr=None):
    # TODO: Fix the doc string. Update descriptions and add return values.
    """Calculates all common error terms, returning them in a named tuple.

    Args:
        observed_rrs: The observed reflectance(remotely-sensed).
        modelled_rrs: The modelled reflectance(remotely-sensed).
        nedr: Optional. Noise equivalent difference in reflectance.

    Returns:
        namedtuple: The error terms in a named tuple:

        - **distance_alpha** -- Describe me!!!
        - **distance_alpha_f** -- Describe me!!!
        - **distance_f** -- Describe me!!!
        - **distance_lsq** -- Describe me!!!
    """

    # LSQ = sum((observed_spectra - modelled_spectra).^2)^0.5;
    lsq = np.power(
        np.sum(
            np.power(
                observed_rrs -
                modelled_rrs,
                2)),
        0.5)

    if nedr is not None:
        # deliberately avoiding an in-place divide as I want a copy of the
        # spectra to avoid side-effects due to pass by reference semantics
        observed_rrs = observed_rrs / nedr
        modelled_rrs = modelled_rrs / nedr

    f_val = np.power(
        np.sum(
            np.power(
                observed_rrs -
                modelled_rrs,
                2)),
        0.5) / np.sum(observed_rrs)

    topline = np.sum(observed_rrs * modelled_rrs)
    botline1 = np.power(np.sum(np.power(observed_rrs, 2)), 0.5)
    botline2 = np.power(np.sum(np.power(modelled_rrs, 2)), 0.5)

    rat = (topline / (botline1 * botline2)
           if botline1 > 0 and botline2 > 0
           else 0)

    alpha_val = np.arccos(rat) if rat <= 1.0 else 100.0

    results = namedtuple('SambucaErrors',
                         ['distance_alpha',
                          'distance_alpha_f',
                          'distance_f',
                          'distance_lsq'])
    results.distance_lsq = lsq
    results.distance_alpha = alpha_val
    results.distance_f = f_val
    results.distance_alpha_f = f_val * alpha_val

    return results

def distance_alpha(observed_rrs, modelled_rrs, nedr=None):
    # TODO: complete the description
    """Calculates TODO

    Args:
        observed_rrs: The observed reflectance(remotely-sensed).
        modelled_rrs: The modelled reflectance(remotely-sensed).
        noise: Optional spectral noise values.

    Returns:
        - **distance_alpha** -- Describe me!!!
    """
    return error_all(observed_rrs, modelled_rrs, nedr).distance_alpha

def distance_alpha_f(observed_rrs, modelled_rrs, nedr=None):
    # TODO: complete the description
    """Calculates TODO

    Args:
        observed_rrs: The observed reflectance(remotely-sensed).
        modelled_rrs: The modelled reflectance(remotely-sensed).
        noise: Optional spectral noise values.

    Returns:
        - **distance_alpha_f** -- Describe me!!!
    """
    return error_all(observed_rrs, modelled_rrs, nedr).distance_alpha_f

def distance_lsq(observed_rrs, modelled_rrs, nedr=None):
    # TODO: complete the description
    """Calculates TODO

    Args:
        observed_rrs: The observed reflectance(remotely-sensed).
        modelled_rrs: The modelled reflectance(remotely-sensed).
        noise: Optional spectral noise values.

    Returns:
        - **distance_lsq** -- Describe me!!!
    """
    return error_all(observed_rrs, modelled_rrs, nedr).distance_lsq

def distance_f(observed_rrs, modelled_rrs, nedr=None):
    # TODO: complete the description
    """Calculates TODO

    Args:
        observed_rrs: The observed reflectance(remotely-sensed).
        modelled_rrs: The modelled reflectance(remotely-sensed).
        noise: Optional spectral noise values.

    Returns:
        - **distance_f** -- Describe me!!!
    """
    return error_all(observed_rrs, modelled_rrs, nedr).distance_f
