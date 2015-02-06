# Ensure compatibility of Python 2 with Python 3 constructs
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)

import sambuca as sb
import numpy as np
import spectral.io.envi as envi
from scipy.io import loadmat
from pkg_resources import resource_filename


class TestSensorFilter(object):

    ''' Additional sensor filter tests. See test_spectral_resampling.py as well.
    '''

    def setup_method(self, method):
        # load the test data

        # sensor filter
        self.__qb_sensor_filter = envi.open(
            resource_filename(
                sb.__name__,
                'tests/data/qbtest_filter_350_900nm.hdr'),
            resource_filename(
                sb.__name__,
                'tests/data/qbtest_filter_350_900nm.lib'))

        # input spectra
        self.__qb_input_spectra = envi.open(
            resource_filename(
                sb.__name__,
                'tests/data/qbtest_input_spectra.hdr'),
            resource_filename(
                sb.__name__,
                'tests/data/qbtest_input_spectra.lib'))

        # output spectra
        self.__qb_output_spectra = envi.open(
            resource_filename(
                sb.__name__,
                'tests/data/qbtest_output_spectra.hdr'),
            resource_filename(
                sb.__name__,
                'tests/data/qbtest_output_spectra.lib'))

    def test_validate_data(self):
        assert self.__qb_sensor_filter.spectra.shape == (4, 551)
        assert self.__qb_input_spectra.spectra.shape == (1, 551)
        assert self.__qb_output_spectra.spectra.shape == (1, 4)

    def test_quickbird_spectral_library(self):
        # get the spectral library values as numpy arrays
        sensor_filter = self.__qb_sensor_filter.spectra
        input_spectra = self.__qb_input_spectra.spectra[0]
        expected_output = self.__qb_output_spectra.spectra[0]
        actual_output = sb.apply_sensor_filter(input_spectra, sensor_filter)
        assert np.allclose(
            actual_output,
            expected_output,
            rtol=1.e-5,
            atol=1.e-20)

    def test_synthetic_matlab_data(self):
        # load the test values generated from the Matlab code
        filename = resource_filename(
            sb.__name__,
            'tests/data/test_resample.mat')
        self.__data = loadmat(filename, squeeze_me=True)

        src_spectra = self.__data['modelled_spectra']
        expected_spectra = self.__data['resampled_spectra']

        # the matlab sensor filter is transposed relative to layout that the
        # Sambuca code expects
        sensor_filter = self.__data['filt'].transpose()

        assert sensor_filter.shape[0] == 36
        assert sensor_filter.shape[1] == 551

        # resample
        resampled_spectra = sb.apply_sensor_filter(src_spectra, sensor_filter)

        # test
        assert expected_spectra.shape == resampled_spectra.shape
        assert np.allclose(expected_spectra, resampled_spectra)
