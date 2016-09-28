from unittest import TestCase, mock

from pushwoosh import client


class CreateMessageTestCase(TestCase):

    test_application = 'application'
    test_auth_token = 'auth_token'
    test_content = {'ru': 'test content'}
    test_filters = {'filter': 'test_filter'}
    test_params = {'color': 'red'}
    ok_response = {'status_code': 200, 'status_message': 'Ok!'}
    fail_response = {'status_code': 404, 'status_message': 'error'}

    def test_create_message(self):
        request_sender = mock.create_autospec(client._send_request)
        request_sender.return_value = self.ok_response

        client.create_message(
            application=self.test_application,
            auth_token=self.test_auth_token,
            content=self.test_content,
            params=self.test_params,
            filters=self.test_filters,
            request_sender=request_sender
        )

        request = request_sender.call_args[0][0]
        notification = request['request']['notifications'][0]

        assert notification['content'] == self.test_content

        for name, op, value in notification['conditions']:
            assert op == 'EQ'
            assert value == self.test_filters[name]

        for k, v in self.test_params.items():
            assert notification[k] == v

    def test_responce_error(self):
        request_sender = mock.create_autospec(client._send_request)
        request_sender.return_value = self.fail_response

        with self.assertRaises(client.RequestError):
            client.create_message(
                application=self.test_application,
                auth_token=self.test_auth_token,
                content=self.test_content,
                request_sender=request_sender,
            )


class RequestErrorTestCase(TestCase):

    def test(self):
        exc = client.RequestError({
            'status_code': 404,
            'status_message': 'error',
        })
        assert str(exc) == '404, error'


class MakeConditionsTestCase(TestCase):

    def test(self):
        res = client._make_conditions({
            'scalar': 'value',
            'list': [1, 2, 3],
        })
        assert sorted(res) == [
            ['list', 'IN', [1, 2, 3]],
            ['scalar', 'EQ', 'value'],
        ]


class CreateNotificationTestCase(TestCase):

    def test(self):
        test_data = {
            'content': {'ru': 'test'},
            'filters': {'filter': 'test_filter'},
            'params': {'color': 'red'},
        }

        notification = client._create_notification(**test_data)

        assert notification['content'] == test_data['content']
        assert notification['send_date'] == 'now'

        for name, _, value in notification['conditions']:
            assert value == test_data['filters'][name]

        for k, v in test_data['params'].items():
            assert notification[k] == v
