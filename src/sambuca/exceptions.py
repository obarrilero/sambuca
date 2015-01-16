""" Sambuca exception definitions.
"""
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


class SambucaException(Exception):
    """Root exception class for Sambuca exceptions.

    Only used as a base class for any Sambuca errors.
    This exception is never raised directly.
    """
    pass


class UnsupportedDataFormatError(SambucaException):
    """The file format is not supported by Sambuca."""
    pass
