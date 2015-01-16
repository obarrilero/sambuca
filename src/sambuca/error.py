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
from builtins import *

from collections import namedtuple
import numpy as np


def error_all(observed_spectra, modelled_spectra, noise=None):
    # TODO: Fix the doc string. Update descriptions and add return values.
    """Calculates all common error terms, returning them in a named tuple.

    Args:
        observed_spectra: The observed spectra.
        modelled_spectra: The modelled spectra.
        noise: Optional spectral noise values.

    Returns:
        A named tuple of error values:

        ================ ==============
        Error Term       Description
        ================ ==============
        distance_alpha   Describe me!!!
        distance_alpha_f Describe me!!!
        distance_f       Describe me!!!
        distance_lsq     Describe me!!!
        error_af         Describe me!!!
        ================ ==============
    """

    # LSQ = sum((observed_spectra - modelled_spectra).^2)^0.5;
    lsq = np.power(
        np.sum(
            np.power(
                observed_spectra -
                modelled_spectra,
                2)),
        0.5)

    if noise is not None:
        # deliberately avoiding an in-place divide as I want a copy of the
        # spectra to avoid side-effects due to pass by reference semantics
        observed_spectra = observed_spectra / noise
        modelled_spectra = modelled_spectra / noise

    f_val = np.power(
        np.sum(
            np.power(
                observed_spectra -
                modelled_spectra,
                2)),
        0.5) / np.sum(observed_spectra)

    topline = np.sum(observed_spectra * modelled_spectra)
    botline1 = np.power(np.sum(np.power(observed_spectra, 2)), 0.5)
    botline2 = np.power(np.sum(np.power(modelled_spectra, 2)), 0.5)

    rat = (topline / (botline1 * botline2)
           if botline1 > 0 and botline2 > 0
           else 0)

    alpha_val = np.arccos(rat) if rat <= 1.0 else 100.0

    results = namedtuple('SambucaErrors',
                         ['distance_alpha',
                          'distance_alpha_f',
                          'distance_f',
                          'distance_lsq',
                          'error_af'])
    results.distance_lsq = lsq
    results.distance_alpha = alpha_val
    results.distance_f = f_val
    results.distance_alpha_f = f_val * alpha_val
    # error_a = alpha_val
    # error_f = f_val
    # TODO: why is this fudge factor added to alpha_val?
    results.error_af = f_val*(0.00000001+alpha_val)

    return results
