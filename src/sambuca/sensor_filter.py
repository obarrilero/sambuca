""" Contains functions for working with Sensor Filters.
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

import numpy as np


# TODO: Do I need to rename this function?
def apply_sensor_filter(spectra, filter_):
    """Resamples a remotely-sensed reflectance spectra using the given spectral
    sensitivity curves.

    Args:
        spectra (array-like): The input reflectance spectra.
        filter_ (matrix-like): The spectral sensitivity matrix.
            The first dimension determines the number of output bands.
            The second dimension represents the proportional contribution of
            each of the input bands to an output band. The size must match the
            number of bands in the input spectra.

    Returns:
        ndarray: The resampled spectra.

    """

    return np.dot(filter_, spectra) / filter_.sum(1)
