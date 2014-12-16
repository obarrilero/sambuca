# Ensure compatibility of Python 2 with Python 3 constructs
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import range

import sambuca as sb
import numpy as np
from scipy.io import loadmat
from pkg_resources import resource_filename


class TestErrorFunctions(object):

    """ Test the error functions used to assess model closure
    """

    def setup_method(self, method):
        # load the test values generated from the Matlab code
        filename = resource_filename(
            sb.__name__,
            'tests/data/test_error_noise.mat')
        self.__noisedata = loadmat(filename, squeeze_me=True)

        filename = resource_filename(
            sb.__name__,
            'tests/data/test_error_no_noise.mat')
        self.__data = loadmat(filename, squeeze_me=True)

    def unpack_data(self, data):
        return (data['observed_spectra'],
                data['modelled_spectra'],
                data['noiserrs'],
                data['num_bands'],
                data['distance_alpha'],
                data['distance_alpha_f'],
                data['distance_f'],
                data['distance_lsq'],
                data['error_a'],
                data['error_af'],
                data['error_f'])

    def validate_data(self, data):
        data_ = self.unpack_data(data)
        os = data_[0]
        ms = data_[1]
        noise = data_[2]
        num_bands = data_[3]
        assert os.shape[0] == num_bands
        assert ms.shape[0] == num_bands
        assert noise.shape[0] == num_bands
        assert noise.shape[0] == num_bands

    def test_validate_no_noise_data(self):
        self.validate_data(self.__data)

    def test_validate_noise_data(self):
        self.validate_data(self.__noisedata)
