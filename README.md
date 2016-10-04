# Pushwoosh
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Afonasev/PushWoosh/edit/master/LICENSE)
[![Build Status](https://travis-ci.org/Afonasev/PushWoosh.svg?branch=master)](https://travis-ci.org/Afonasev/pushwoosh)
[![Coverage Status](https://coveralls.io/repos/github/Afonasev/PushWoosh/badge.svg?branch=master)](https://coveralls.io/github/Afonasev/PushWoosh?branch=master)

## Installing
```
$ pip install git+https://github.com/Afonasev/pushwoosh
```

## Initialize client
```python
>>> from pushwoosh import Client
>>> client = Clinet(auth_token='AUTH_TOKEN', application='APPLICATION_CODE')
```

## Client api
```python

class Client:

    def __init__(self, auth_token, application, log=dummy_logger):
        ...

    def create_message(self, content, params=None, filters=None):
        """
        :type content: dict[str, str]
        :type params: dict[str, Any]
        :type filters: dict[str, Any]
        """

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

    def create_cluster(self, name, cooldown=60):
        """
        :type name: str
        :type cooldown: int, silent period after sending notification (seconds)
        :return str, cluster_id
        """

    def delete_cluster(self, cluster_id):
        """
        :type cluster_id: str
        """

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

    def delete_zones(self, zone_ids):
        """
        :type zone_ids: List[int]
        """
```

## Running the testsuite

The minimal requirement for running the testsuite is ``pytest``.  You can
install it with::

    pip install pytest

Then you can run the testsuite with::

    py.test
