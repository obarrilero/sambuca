import sambuca


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

    def test_version(self):

        assert(sambuca.__version__ == '0.1.0')
