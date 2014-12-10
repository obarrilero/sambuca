''' Sambuca exception definitions
'''


class SambucaException(Exception):
    '''Root exception class for Sambuca exceptions.
    Only used to except any Sambuca errors. This exception is never raised.
    '''
    pass


class UnsupportedDataFormatError(SambucaException):
    '''The file format is not supported by Sambuca.
    '''
    pass
