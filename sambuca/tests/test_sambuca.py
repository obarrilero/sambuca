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
