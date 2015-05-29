from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import sambuca as sb
import numpy as np
from scipy.io import readsav
from pkg_resources import resource_filename


class TestErrorFunctions(object):
    """ Test the error functions used to assess model closure
    """

    def setup_method(self, method):
        # load the test values generated from the Matlab code
        self.noise_data = readsav(
            resource_filename(
                sb.__name__,
                'tests/data/error_data.sav'))

        self.no_noise_data = readsav(
            resource_filename(
                sb.__name__,
                'tests/data/no_noise_error_data.sav'))

    @staticmethod
    def unpack_data(data):
        return (data['realrrs'],
                data['rrs'],
                data['noiserrs'],
                data['lsq'],
                data['error_a'],
                data['error_af'],
                data['error_f'])

    def validate_data(self, data):
        unpacked_data = self.unpack_data(data)
        observed = unpacked_data[0]
        modelled = unpacked_data[1]
        noise = unpacked_data[2]
        num_bands = len(observed)
        assert observed.shape[0] == num_bands
        assert modelled.shape[0] == num_bands
        assert noise.shape[0] == num_bands
        assert noise.shape[0] == num_bands

    def test_validate_no_noise_data(self):
        self.validate_data(self.no_noise_data)

    def test_validate_noise_data(self):
        self.validate_data(self.noise_data)

    def test_error_no_noise(self):
        observed, modelled, _, expected_lsq, expected_distance_a, \
            expected_distance_af, expected_distance_f \
            = self.unpack_data(self.no_noise_data)

        actual = sb.error_all(observed, modelled)

        assert np.allclose(actual.distance_alpha, expected_distance_a)
        assert np.allclose(actual.distance_alpha_f, expected_distance_af)
        assert np.allclose(actual.distance_f, expected_distance_f)
        assert np.allclose(actual.distance_lsq, expected_lsq)

    def test_error_noise(self):
        observed, modelled, nedr, expected_lsq, expected_distance_a, \
            expected_distance_af, expected_distance_f \
            = self.unpack_data(self.noise_data)

        actual = sb.error_all(observed, modelled, nedr)

        assert np.allclose(actual.distance_alpha, expected_distance_a)
        assert np.allclose(actual.distance_alpha_f, expected_distance_af)
        assert np.allclose(actual.distance_f, expected_distance_f)
        assert np.allclose(actual.distance_lsq, expected_lsq)

    def test_distance_alpha_noise(self):
        observed = self.noise_data['realrrs']
        modelled = self.noise_data['rrs']
        nedr = self.noise_data['noiserrs']
        expected = self.noise_data['error_a']

        actual = sb.distance_alpha(observed, modelled, nedr)

        assert np.allclose(actual, expected)

    def test_distance_alpha_f_noise(self):
        observed = self.noise_data['realrrs']
        modelled = self.noise_data['rrs']
        nedr = self.noise_data['noiserrs']
        expected = self.noise_data['error_af']

        actual = sb.distance_alpha_f(observed, modelled, nedr)

        assert np.allclose(actual, expected)

    def test_distance_f_noise(self):
        observed = self.noise_data['realrrs']
        modelled = self.noise_data['rrs']
        nedr = self.noise_data['noiserrs']
        expected = self.noise_data['error_f']

        actual = sb.distance_f(observed, modelled, nedr)

        assert np.allclose(actual, expected)

    def test_distance_lsq_noise(self):
        observed = self.noise_data['realrrs']
        modelled = self.noise_data['rrs']
        nedr = self.noise_data['noiserrs']
        expected = self.noise_data['lsq']

        actual = sb.distance_lsq(observed, modelled, nedr)

        assert np.allclose(actual, expected)
