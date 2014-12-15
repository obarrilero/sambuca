''' Sambuca Error Functions.
    Used when assessing model closure during parameter optimisation
'''
# Ensure compatibility of Python 2 with Python 3 constructs
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=redefined-builtin
from builtins import *

import numpy as np


def lsq_no_noise(observed_spectra, modelled_spectra):
    # TODO: Fix the doc string. Needs a real reference to the Mobley paper.
    # TODO: Can I implement a single function that has noise spectra as an optional argument?
    """lsq_no_noise LSQ as in equation 1 of Mobley 2005 AO:i.e. without using
    Noise

    :param observed_spectra: Array-like. The observed spectra
    :param modelled_spectra: Array-like. The modelled spectra
    """
    pass
