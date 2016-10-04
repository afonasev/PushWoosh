from unittest import TestCase

from pushwoosh import errors


class RequestErrorTestCase(TestCase):

    def test(self):
        exc = errors.RequestError({
            'status_code': 404,
            'status_message': 'error',
        })
        assert str(exc) == '404, error'
