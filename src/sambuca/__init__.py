""" Sambuca modeling system
"""

from .exceptions import SambucaException, UnsupportedDataFormatError
from .forward_model import forward_model
from .sensor_filter import apply_sensor_filter
from .error import \
    error_all, \
    distance_alpha, \
    distance_f, \
    distance_lsq, \
    distance_alpha_f


# Versioning: major.minor.patch
# major: increment on a major version. Must be changed when the API changes in
# an imcompatible way.
# minor: new functionality that does not break the
# existing API.
# patch: bug-fixes that do not change the public API
__version__ = '0.1.0'
