from unittest import TestCase, mock

from pushwoosh import client as push_client, errors


OK_RESPONSE = {'status_code': 200, 'status_message': 'OK'}


def ok_with(v):
    ok_response = OK_RESPONSE.copy()
    ok_response['response'] = v
    return ok_response


class PushClientTestCase(TestCase):

    test_content = {'ru': 'test content'}
    test_filters = {'geoid': 1, 'group': 'test'}
    test_params = {'color': 'red', 'my_test_params': 1}

    def test_create_message(self):
        client, execute_method = self._create_client(OK_RESPONSE)

        client.create_message(
            content=self.test_content,
            params=self.test_params,
            filters=self.test_filters,
        )

        url, request = execute_method.call_args[0]
        notification = request['request']['notifications'][0]

        assert url.endswith('createMessage')
        assert notification['content'] == self.test_content

        for name, op, value in notification['conditions']:
            assert op == 'EQ'
            assert value == self.test_filters[name]

        for k, v in self.test_params.items():
            assert notification[k] == v

    def test_create_cluster(self):
        test_cluster_id = 'cluster_id'
        test_cluster_name = 'cluster_name'
        test_cooldown = 100

        self._check_method(
            method='create_cluster',
            kwargs={
                'name': test_cluster_name,
                'cooldown': test_cooldown,
            },
            response={'GeoZoneCluster': test_cluster_id},
            expected_request={
                'name': test_cluster_name,
                'cooldown': test_cooldown,
            },
            expected_result=test_cluster_id,
        )

    def test_delete_cluster(self):
        test_cluster_id = 'cluster_id'

        self._check_method(
            method='delete_cluster',
            kwargs={'cluster_id': test_cluster_id},
            expected_request={'geoZoneCluster': test_cluster_id},
        )

    def test_create_zones(self):
        test_zones = [{
            'content': 'Lorem ipsum',
            'lat': '40.70087797',
            'lng': '-73.931851387',
            'range': 100,
            'name': 'test',
            'cooldown': 60,
        }]
        test_zone_ids = [1]

        self._check_method(
            method='create_zones',
            kwargs={'zones': test_zones},
            response={'GeoZones': test_zone_ids},
            expected_request={'geozones': test_zones},
            expected_result=test_zone_ids,
        )

    def test_delete_zones(self):
        test_zone_ids = [1, 2, 3]

        self._check_method(
            method='delete_zones',
            kwargs={'zone_ids': test_zone_ids},
            expected_request={'geozones': test_zone_ids},
        )

    def test_get_clusters(self):
        test_clusters = [{
            'name': 'Cluster on Times',
            'code': 'AE2C4-4E070',
            'cooldown': 86400,
            'geozones': 1,
        }]

        self._check_method(
            method='get_clusters',
            response={'clusters': test_clusters},
            expected_result=test_clusters,
        )

    def test_get_zones(self):
        test_zones_by_cluster = [{
            'name': 'cluster_name',
            'GeoZones': [{
                'content': 'Lorem ipsum',
                'lat': '40.70087797',
                'lng': '-73.931851387',
            }],
        }]

        self._check_method(
            method='get_zones',
            response={'clusters': test_zones_by_cluster},
            expected_result=test_zones_by_cluster,
        )

    def test_responce_error_code(self):
        client, _ = self._create_client(
            {'status_code': 404, 'status_message': 'OK'},
        )

        with self.assertRaises(errors.RequestError):
            client.create_message(self.test_content)

    def test_responce_no_ok_message(self):
        client, _ = self._create_client(
            {'status_code': 200, 'status_message': 'error'},
        )

        with self.assertRaises(errors.RequestError):
            client.create_message(self.test_content)

    def _create_client(self, return_value):
        client = push_client.Client('', '')
        client._execute_request = mock.create_autospec(
            client._execute_request,
            return_value=return_value,
        )
        return client, client._execute_request

    def _check_method(
        self,
        method,
        kwargs=None,
        response=None,
        expected_request=None,
        expected_result=None,
    ):
        if kwargs is None:
            kwargs = {}

        client, execute_method = self._create_client(ok_with(response))
        result = getattr(client, method)(**kwargs)

        if expected_result is not None:
            assert result == expected_result

        if expected_request is not None:
            _, request = execute_method.call_args[0]
            self._check_request(request, expected_request)

    def _check_request(self, request, test_data):
        body = request['request']
        body.pop('auth')
        body.pop('application')
        assert body == test_data


class MakeConditionsTestCase(TestCase):

    def test(self):
        res = push_client._make_conditions({
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

        notification = push_client._create_notification(**test_data)

        assert notification['content'] == test_data['content']
        assert notification['send_date'] == 'now'

        for name, _, value in notification['conditions']:
            assert value == test_data['filters'][name]

        for k, v in test_data['params'].items():
            assert notification[k] == v
