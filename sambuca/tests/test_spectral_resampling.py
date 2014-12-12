import sambuca as sb
import numpy as np
from scipy.io import loadmat
from pkg_resources import resource_filename


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
        assert False
        # expected_spectra = self.__data['modelled_spectra']

        # modelled_spectra = sb.forward_model(
            # chl=self.__data['chl'],
            # cdom=self.__data['cdom'],
            # tr=self.__data['tr'],
            # h=self.__data['h'],
            # q=self.__data['q'],
            # substrate1=self.__data['substrate1'],
            # substrate2=self.__data['substrate2'],
            # wav=self.__data['wav'],
            # awater=self.__data['awater'],
            # aphy_star=self.__data['aphy_star'],
            # d_wls=self.__data['d_wls'],)

        # assert np.allclose(
            # modelled_spectra,
            # expected_spectra,
            # rtol=1.e-5,
            # atol=1.e-20)
