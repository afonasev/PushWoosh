from unittest import TestCase

from pushwoosh import utils


class DumpsTestCase(TestCase):

    def test(self):
        assert utils.dumps({'test': 'test'}) == '{"test": "test"}'
