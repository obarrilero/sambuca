""" Contains functions for working with Sensor Filters.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import numpy as np


# TODO: Do I need to rename this function?
def apply_sensor_filter(spectra, response_function):
    """Resamples a remotely-sensed reflectance spectra using the given spectral
    response function.

    Args:
        spectra (array-like): The input reflectance spectra.
        response_function (matrix-like): The spectral sensitivity matrix.
            The first dimension determines the number of output bands.
            The second dimension represents the proportional contribution of
            each of the input bands to an output band. The size must match the
            number of bands in the input spectra.

    Returns:
        ndarray: The resampled spectra.

    """

    return np.dot(response_function, spectra) / response_function.sum(1)
