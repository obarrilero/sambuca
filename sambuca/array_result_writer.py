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
                this contains the final parameters; otherwise None.
        """

        super().__call__(x, y, observed_rrs, parameters)

        # If this pixel did not converge, then there is nothing more to do
        if not parameters:
            return

        # Generate results from the given parameters
        model_results = sbc.forward_model(
            parameters.chl,
            parameters.cdom,
            parameters.nap,
            parameters.depth,
            self._fixed_parameters.substrate1,
            self._fixed_parameters.wavelengths,
            self._fixed_parameters.a_water,
            self._fixed_parameters.a_ph_star,
            self._fixed_parameters.num_bands,
            substrate_fraction=parameters.substrate_fraction,
            substrate2=parameters.substrate2,
            a_cdom_slope=parameters.a_cdom_slope,
            a_nap_slope=parameters.a_nap_slope,
            bb_ph_slope=parameters.bb_ph_slope,
            bb_nap_slope=parameters.bb_nap_slope,
            lambda0cdom=parameters.lambda0cdom,
            lambda0nap=parameters.lambda0nap,
            lambda0x=parameters.lambda0x,
            x_ph_lambda0x=parameters.x_ph_lambda0x,
            x_nap_lambda0x=parameters.x_nap_lambda0x,
            a_cdom_lambda0cdom=parameters.a_cdom_lambda0cdom,
            a_nap_lambda0nap=parameters.a_nap_lambda0nap,
            bb_lambda_ref=parameters.bb_lambda_ref,
            water_refractive_index=parameters.water_refractive_index,
            theta_air=parameters.theta_air,
            off_nadir=parameters.off_nadir,
            q_factor=parameters.q_factor)

        closed_rrs = sbc.apply_sensor_filter(
            model_results.rrs,
            self._sensor_filter)

        error = sbc.error_all(observed_rrs, closed_rrs, self._nedr)

        # Write the results into our arrays
        self.error_alpha[x,y] = error.alpha
        self.error_alpha_f[x,y] = error.alpha_f
        self.error_f[x,y] = error.f
        self.error_lsq[x,y] = error.lsq
        self.chl[x,y] = parameters.chl
        self.cdom[x,y] = parameters.cdom
        self.nap[x,y] = parameters.nap
        self.depth[x,y] = parameters.depth
        self.closed_rrs[:,x,y] = closed_rrs
