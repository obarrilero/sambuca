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

    def test_scipy_resampling(self):
        # I know this test fails. Keep the code for reference, but skip the test
        pytest.skip()

        # grab the data
        src_spectra = self.__data['modelled_spectra']
        expected_spectra = self.__data['resampled_spectra']
        destination_bands = len(expected_spectra)

        # resample
        resampled_spectra = resample(src_spectra, destination_bands)

        # test
        assert len(expected_spectra) == len(resampled_spectra)
        assert np.allclose(expected_spectra, resampled_spectra)

    def test_apply_sensor_filter(self):
        src_spectra = self.__data['modelled_spectra']
        expected_spectra = self.__data['resampled_spectra']
        destination_bands = len(expected_spectra)
        sensor_filter = self.__data['filt']
        assert sensor_filter.shape[0] == 551
        assert sensor_filter.shape[1] == 36

        # resample
        resampled_spectra = sb.apply_sensor_filter(src_spectra, sensor_filter)

        # test
        assert len(expected_spectra) == len(resampled_spectra)
        assert np.allclose(expected_spectra, resampled_spectra)
