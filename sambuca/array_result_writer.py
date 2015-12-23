""" Pixel result handler that writes model outputs to numpy arrays.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import numpy as np

from .pixel_result_handler import PixelResultHandler


class ArrayResultWriter(PixelResultHandler):
    """ Pixel result handler that writes pixel model outputs
    to numpy ndarrays.

    Note that the current implementation is writing a hard-coded set of outputs
    for the alpha implementation. The intention is to replace this with a
    data-driven system that only captures the outputs specified by the user.

    """

    def __init__(
            self,
            width,
            height,
            sensor_filter,
            nedr,
            fixed_parameters):
        """
        Initialise the ArrayWriter.
        Args:
            width (int): Width in pixels of the modelled region.
            height (int): Height in pixels of the modelled region.
            sensor_filter (array-like): The Sambuca sensor filter.
            nedr (array-like): Noise equivalent difference in reflectance.
            fixed_parameters (sambuca.AllParameters): The fixed model
                parameters.
        """
        super().__init__()

        self._width = width
        self._height = height
        self._sensor_filter = sensor_filter
        self._nedr = nedr
        self._num_modelled_bands = sensor_filter.shape[1]
        self._num_observed_bands = sensor_filter.shape[0]
        self._fixed_parameters = fixed_parameters

        # initialise the ndarrays for the outputs.
        # Note that I am hard-coding these outputs for now, but the intent is that this class
        # support a customisable list of outputs.
        self.error_alpha = np.zeros((width, height))
        self.error_alpha_f = np.zeros((width, height))
        self.error_f = np.zeros((width, height))
        self.error_lsq = np.zeros((width, height))
        self.chl = np.zeros((width, height))
        self.cdom = np.zeros((width, height))
        self.nap = np.zeros((width, height))
        self.depth = np.zeros((width, height))
        self.substrate_fraction = np.zeros((width, height))
        self.closed_rrs = np.zeros((self._num_observed_bands, width, height))

    def __call__(self, x, y, observed_rrs, parameters=None):
        """
        Called by the parameter estimator when there is a result for a pixel.

        Args:
            x (int): The pixel x coordinate.
            y (int): The pixel y coordinate.
            observed_rrs (array-like): The observed remotely-sensed reflectance
                at this pixel.
            parameters (sambuca.FreeParameters): If the pixel converged,
                the final parameters; otherwise None.
        """

        super().__call__(x, y, observed_rrs, parameters)

        # If this pixel did not converge, then there is nothing more to do
        if not parameters:
            return

        # Generate results from the given parameters
        model_results = sbc.forward_model(
            chl = parameters.chl,
            cdom = parameters.cdom,
            nap = parameters.nap,
            depth = parameters.depth,
            substrate_fraction = parameters.substrate_fraction,

        closed_rrs = sbc.apply_sensor_filter(
            model_results.rrs,
            self._sensor_filter)

        error = sbc.error_all(observed_rrs, closed_rrs, self._nedr)

        # Write the results into our arrays

