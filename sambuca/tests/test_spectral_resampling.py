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
from scipy.signal import resample
from pkg_resources import resource_filename
import pytest


class TestSpectralResampling(object):

    ''' Comparing spectral resampling methods to data from the Matlab reference
    '''

    def setup_method(self, method):
        # load the test values generated from the Matlab code
        filename = resource_filename(
            sb.__name__,
            'tests/data/test_resample.mat')
        self.__data = loadmat(filename, squeeze_me=True)

    def test_validate_data(self):
        assert 'modelled_spectra' in self.__data
        assert 'resampled_spectra' in self.__data
        assert 'filt' in self.__data
        assert 'filtsum' in self.__data

    # def test_scipy_resampling(self):
        # pytest.skip('I know this test fails. Keep the code for reference, but skip the test')

        # # grab the data
        # src_spectra = self.__data['modelled_spectra']
        # expected_spectra = self.__data['resampled_spectra']
        # destination_bands = len(expected_spectra)

        # # resample
        # actual_spectra = resample(src_spectra, destination_bands)

        # # test
        # assert len(expected_spectra) == len(actual_spectra)
        # assert np.allclose(expected_spectra, actual_spectra)

    def test_filter_summation(self):
        ''' Testing my numpy implementation of the Matlab sensor filter summation
        '''
        sensor_filter = self.__data['filt']
        filtsum_expected = self.__data['filtsum']
        src_bands = 551  # d_wls in matlab code
        dst_bands = 36  # n_wls in matlab code

        # pre-test sanity check on expectations
        assert sensor_filter.shape[0] == src_bands
        assert sensor_filter.shape[1] == dst_bands

        # calculate the sum
        filtsum_actual = np.sum(sensor_filter, axis=0)

        # test expectations
        assert filtsum_expected.shape == filtsum_actual.shape
        assert filtsum_actual.shape[0] == dst_bands
        assert np.allclose(filtsum_expected, filtsum_actual)

    def test_band_summation(self):
        ''' Testing my numpy implementation of the Matlab sensor filter band summation
            with no explicit loops
        '''
        src_spectra = self.__data['modelled_spectra']
        sensor_filter = self.__data['filt']
        bandsum_expected = self.__data['bandsum']

        # the loops in the matlab code are actually just a dot product
        bandsum_actual = np.dot(src_spectra, sensor_filter)

        assert np.allclose(bandsum_expected, bandsum_actual)

    def test_apply_sensor_filter(self):
        src_spectra = self.__data['modelled_spectra']
        expected_spectra = self.__data['resampled_spectra']
        sensor_filter = self.__data['filt']
        assert sensor_filter.shape[0] == 551
        assert sensor_filter.shape[1] == 36

        # resample
        resampled_spectra = sb.sensor_filter_ml(src_spectra, sensor_filter)

        # test
        assert expected_spectra.shape == resampled_spectra.shape
        assert np.allclose(expected_spectra, resampled_spectra)
