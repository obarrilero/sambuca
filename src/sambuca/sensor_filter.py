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


def apply_sensor_filter(spectra, filter_):
    """Resamples a spectra using the given spectral response filter.

    Args:
        spectra (array-like): The input spectra.
        filter_ (matrix-like): The spectral response filter matrix.
            The first dimension determines the number of output bands.
            The second dimension must match the number of bands in the input
            spectra.

    Returns:
        ndarray: The resampled spectra.

    """

    return np.dot(filter_, spectra) / filter_.sum(1)
