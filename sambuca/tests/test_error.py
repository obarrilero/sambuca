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
import pytest


class TestErrorFunctions(object):
    """ Test the error functions used to assess model closure
    """

    def setup_method(self, method):
        # load the test values generated from the Matlab code
        filename = resource_filename(
            sb.__name__,
            'tests/data/test_error.mat')
        self.__data = loadmat(filename, squeeze_me=True)

    def test_validate_error_data(self):
        os = self.__data['observed_spectra']
        ms = self.__data['modelled_spectra']
        expected_error = self.__data['error']
        noise = self.__data['nedr_36band']
        num_bands = self.__data['num_bands']
        assert os.shape[0] == num_bands
        assert ms.shape[0] == num_bands
        assert expected_error.shape[0] == num_bands
        assert noise.shape[0] == num_bands

    def lsq_no_noise(self):
        os = self.__data['observed_spectra']
        ms = self.__data['modelled_spectra']
        expected_error = self.__data['error']

        actual_error = sb.error.lsq_no_noise(os, ms)

        np.allclose(expected_error, actual_error, rtol=1.e-5, atol=1.e-20)
