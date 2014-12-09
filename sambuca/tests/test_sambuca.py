import sambuca as sb
import pytest
from scipy.io import loadmat
from pkg_resources import resource_filename


class TestSambuca:

    """Sambuca test class"""

    def setup_class(cls):
        pass

    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_exception(self):
        '''Toy test for Sambuca Exceptions. Really just tests that they exist
        and are exported correctly
        '''
        with pytest.raises(sb.SambucaException) as ex:
            raise sb.SambucaException('pass')
        assert 'pass' in str(ex.value)

    def test_forwardModel(self):
        # load the test values generated from the Matlab code
        filename = resource_filename(__name__, './data/forwardModelTestValues.mat')
        data = loadmat(filename, squeeze_me=True)

        # for readability, alias the dictionary entries
        d_wls = data['d_wls']
        n_wls = data['n_wls']
        wav = data['wav']
        awater = data['awater']
        aphy_star = data['aphy_star']
        q = data['q']
        tr = data['tr']
        h = data['h']
        chl = data['chl']
        cdom = data['cdom']
        substrate1 = data['substrate1']
        substrate2 = data['substrate2']
        expected_spectra = data['modelled_spectra']

        assert len(awater) == d_wls
