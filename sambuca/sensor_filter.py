''' Sambuca Sensor Filtering
'''
import numpy as np


def sensor_filter_ml(spectra, filter_):
    # TODO: fix this function description. My attempt babbles!
    """sensor_filter_ml
    Sensor filter, resamples the input spectra using the spectral
    response function.

    :param spectra: the input spectra
    :param filter_: spectral response function
    """
    # Squelch errors from the well-known issues that pylint has with numpy:
    # pylint: disable=no-member

    return np.dot(spectra, filter_) / filter_.sum(0)
