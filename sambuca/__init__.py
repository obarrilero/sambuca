""" Sambuca modeling system
"""

# import .constants
from .exceptions import SambucaException, UnsupportedDataFormatError
from .forward_model import forward_model, ForwardModelResults
from .sensor_filter import apply_sensor_filter
from .error import \
    error_all, \
    distance_alpha, \
    distance_f, \
    distance_lsq, \
    distance_alpha_f

__author__ = 'Daniel Collins'
__email__ = 'daniel.collins@csiro.au'

# Versioning: major.minor.patch
# major: increment on a major version. Must be changed when the API changes in
# an imcompatible way.
# minor: new functionality that does not break the
# existing API.
# patch: bug-fixes that do not change the public API
__version__ = '0.1.0'
