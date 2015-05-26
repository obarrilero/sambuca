# Ensure compatibility of Python 2 with Python 3 constructs
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

from pkg_resources import resource_filename

import numpy as np
import sambuca as sb
from pytest import fail
from scipy.io import readsav


class TestForwardModel(object):

    """Sambuca forward model test class
    """

    def setup_class(self):
        # load the test values
        filename = resource_filename(
            sb.__name__,
            'tests/data/_F1nm_H25_a_Non_UQ02_MB_RC__OS_SHon.sav')
        self.data = readsav(filename)

    def test_validate_data(self):
        # fail()
        assert self.data

        # bands = self.__data['d_wls']
        # assert len(self.__data['awater']) == bands
        # assert len(self.__data['wav']) == bands
        # assert len(self.__data['substrate1']) == bands
        # assert len(self.__data['substrate2']) == bands
        # assert len(self.__data['aphy_star']) == bands

    def test_substrate_r(self):
        fail()

    def test_closed_spectrum(self):
        fail()

    def test_closed_deep_spectrum(self):
        fail()

    def test_kd(self):
        fail()

    def test_kub(self):
        fail()

    def test_kuc(self):
        fail()

    # def test_forward_model_against_matlab_results(self):
        # expected_spectra = self.__data['modelled_spectra']

        # modelled_spectra = sb.forward_model(
            # chl=self.__data['chl'],
            # cdom=self.__data['cdom'],
            # nap=self.__data['tr'],
            # h=self.__data['h'],
            # q=self.__data['q'],
            # substrate1=self.__data['substrate1'],
            # substrate2=self.__data['substrate2'],
            # wav=self.__data['wav'],
            # awater=self.__data['awater'],
            # aphy_star=self.__data['aphy_star'],
            # num_bands=self.__data['d_wls'],)

        # assert np.allclose(
            # modelled_spectra,
            # expected_spectra,
            # rtol=1.e-5,
            # atol=1.e-20)
