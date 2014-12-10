""" Sambuca modeling system
"""

# import the exceptions
from .exceptions import SambucaException, UnsupportedDataFormatError

# import the forward model
from .forward_model import ForwardModel

# import everything else
from . import sambuca

# Versioning: major.minor.patch
# major: increment on a major version. Must be changed when the API changes in an imcompatible way.
# minor: new functionality that does not break the existing API.
# patch: bug-fixes that do not change the public API
__version__ = '0.1.0'
