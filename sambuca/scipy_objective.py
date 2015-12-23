""" Objective function for parameter estimation using scipy minimisation.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

from collections.abc import Callable

import sambuca_core as sbc


class SciPyObjective(Callable):
    """
    Configurable objective function for Sambuca parameter estimation, intended
    for use with the SciPy minimisation methods.

    Attributes:
        observed_rrs (array-like): The observed remotely-sensed reflectance.
            This attribute must be updated when you require the objective
            instance to use a different value.
    """

    def __init__(
            self,
            sensor_filter,
            fixed_parameters,
            nedr=None):
        """
        Initialise the ArrayWriter.
        Args:
            sensor_filter (array-like): The Sambuca sensor filter.
            fixed_parameters (sambuca.AllParameters): The fixed model
                parameters.
            nedr (array-like): Noise equivalent difference in reflectance.
        """
        super().__init__()

        self._sensor_filter = sensor_filter
        self._nedr = nedr
        self._fixed_parameters = fixed_parameters
        self.observed_rrs = None

    def __call__(self, parameters):
        """
        Returns an objective score for the given parameter set.

        Args:
            parameters (tuple): The parameter tuple
                (chl, cdom, nap, substrate_fraction, depth).
        """

        # TODO: do I need to implement this? Here or in a subclass?
        # To support algorithms without support for boundary values, we assign a high
        # score to out of range parameters. This may not be the best approach!!!
        # p_bounds is a tuple of (min, max) pairs for each parameter in p
        '''
        if p_bounds is not None:
            for _p, lu in zip(p, p_bounds):
                l, u = lu
                if _p < l or _p > u:
                    return 100000.0
        '''

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

        # TODO: allow dependency injection of the specific error term to return
        error = sbc.error_all(observed_rrs, closed_rrs, self._nedr)
        return error.f
