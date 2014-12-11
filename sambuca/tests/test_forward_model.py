import sambuca as sb
import numpy as np
from scipy.io import loadmat
from pkg_resources import resource_filename


class TestForwardModel(object):

    """Sambuca forward model test class"""

    def setup_class(cls):
        pass

    def teardown_class(cls):
        pass

    def setup_method(self, method):
        # load the test values generated from the Matlab code
        filename = resource_filename(
            __name__,
            './data/forwardModelTestValues.mat')
        self.__data = loadmat(filename, squeeze_me=True)

    def teardown_method(self, method):
        pass

    def test_validate_data(self):
        bands = self.__data['d_wls']
        assert len(self.__data['awater']) == bands
        assert len(self.__data['wav']) == bands
        assert len(self.__data['substrate1']) == bands
        assert len(self.__data['substrate2']) == bands
        assert len(self.__data['aphy_star']) == bands

    def test_forward_model_against_matlab_results(self):
        expected_spectra = self.__data['modelled_spectra']

        modelled_spectra = sb.forward_model(
            chl=self.__data['chl'],
            cdom=self.__data['cdom'],
            tr=self.__data['tr'],
            h=self.__data['h'],
            q=self.__data['q'],
            substrate1=self.__data['substrate1'],
            substrate2=self.__data['substrate2'],
            wav=self.__data['wav'],
            awater=self.__data['awater'],
            aphy_star=self.__data['aphy_star'],
            d_wls=self.__data['d_wls'],)

        assert np.allclose(
            modelled_spectra,
            expected_spectra,
            rtol=1.e-5,
            atol=1.e-20)
