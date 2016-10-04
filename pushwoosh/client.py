import json
import unittest.mock
import urllib.parse
import urllib.request

from . import errors
from . import utils


API_CREATE_MESSAGE = 'https://cp.pushwoosh.com/json/1.3/createMessage'
API_GET_CLUSTERS = 'https://cp.pushwoosh.com/json/1.3/listGeoZoneClusters'
API_ADD_CLUSTER = 'https://cp.pushwoosh.com/json/1.3/addGeoZoneCluster'
API_DELETE_CLUSTER = 'https://cp.pushwoosh.com/json/1.3/deleteGeoZoneCluster'
API_GET_ZONES = 'https://cp.pushwoosh.com/json/1.3/listGeoZones'
API_ADD_ZONE = 'https://cp.pushwoosh.com/json/1.3/addGeoZone'
API_DELETE_ZONE = 'https://cp.pushwoosh.com/json/1.3/deleteGeoZone'

dummy_logger = unittest.mock.Mock()


class Client:

    def __init__(self, auth_token, application, log=dummy_logger):
        self._auth_token = auth_token
        self._application = application
        self._log = log

    def create_message(self, content, params=None, filters=None):
        """
        :type content: dict[str, str]
        :type params: dict[str, Any]
        :type filters: dict[str, Any]
        """
        notification = _create_notification(content, filters, params)
        self._send(API_CREATE_MESSAGE, {'notifications': [notification]})
        self._log.info('Notification (%s) pushed', utils.dumps(notification))

    def get_clusters(self):
        """
        :return list of clusters
            example:
            [{
                'name': 'Cluster on Times',
                'code': 'AE2C4-4E070',
                'cooldown': 86400,
                'geozones': 1,
            }]
        """
        response = self._send(API_GET_CLUSTERS)
        return response['response']['clusters']

    def create_cluster(self, name, cooldown=60):
        """
        :type name: str
        :type cooldown: int, silent period after sending notification (seconds)
        :return str, cluster_id
        """
        body = {'name': name, 'cooldown': cooldown}
        response = self._send(API_ADD_CLUSTER, body)
        cluster_id = response['response']['GeoZoneCluster']
        self._log.info('Zone cluster (%s) created, id=%r', body, cluster_id)
        return cluster_id

    def delete_cluster(self, cluster_id):
        """
        :type cluster_id: str
        """
        self._send(API_DELETE_CLUSTER, {'geoZoneCluster': cluster_id})
        self._log.info('Zone cluster deleted, id=%r', cluster_id)

    def get_zones(self):
        """
        :return List[Dict], zones grouped by cluster
            example:
            [{
                'name': 'Cluster',
                'geoZones': [{
                    'name': 'Geozone 1',
                    'lat': 52.26816,
                    'lng': -109.6875,
                    'cooldown': 86340,
                    'range': 100,
                    'presetCode': null,
                    'content': {
                         'default': 'Push for Geozone 1'
                    }
                }],
            }]
        """
        response = self._send(API_GET_ZONES)
        return response['response']['clusters']

    def create_zones(self, zones):
        """
        :type zones: List[Dict]
            zone example:
            {
                'content': 'Lorem ipsum',  # or dict with language as key
                'lat': '40.70087797',
                'lng': '-73.931851387',

                # Optional
                'cluster': 'CLUSTER ID',
                'name': 'ZONE NAME',
                'range': 50,  # geozone range. In meters, from 50 to 1000.
                'cooldown': 60,  # silent period after sending, in seconds
            }

        :return List[int], zone ids
        """
        for zone in zones:
            for param, default_value in (
                ('name', 'geozone'),
                ('range', 1000),
                ('cooldown', 60),
            ):
                if param not in zone:
                    zone[param] = default_value

        body = {'geozones': zones}
        response = self._send(API_ADD_ZONE, body)
        zone_ids = response['response']['GeoZones']

        self._log.info(
            'Zones (%s) created, ids=%r', utils.dumps(body), zone_ids,
        )

        return response['response']['GeoZones']

    def delete_zones(self, zone_ids):
        """
        :type zone_ids: List[int]
        """
        self._send(API_DELETE_ZONE, {'geozones': zone_ids})
        self._log.info('Zones with id in %r deleted', zone_ids)

    def _send(self, url, body=None):
        request = self._create_request(body)
        response = self._execute_request(url, request)

        if (
            response['status_code'] != 200 or
            response['status_message'] != 'OK'
        ):
            raise errors.RequestError(response)

        return response

    def _create_request(self, body):
        request = {
            'request': {
                'application': self._application,
                'auth': self._auth_token,
            },
        }
        if body is not None:
            request['request'].update(body)
        return request

    @staticmethod
    def _execute_request(url, request):
        req = urllib.request.Request(
            url, json.dumps(request, ensure_ascii=False).encode(),
        )

        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())


def _create_notification(content, filters, params):
    notification = {
        'content': content,
        'send_date': 'now',
    }

    if filters is not None:
        notification['conditions'] = _make_conditions(filters)

    if params is not None:
        for k, v in params.items():
            notification[k] = v

    return notification


def _make_conditions(filters):
    conditions = []

    for k, v in filters.items():
        if isinstance(v, list):
            operator = 'IN'
        else:
            operator = 'EQ'
        conditions.append([k, operator, v])

    return conditions
