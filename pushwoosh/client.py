import json
import urllib.parse
import os

import urllib.request


API_CREATE_MESSAGE_URL = 'https://cp.pushwoosh.com/json/1.3/createMessage'


class RequestError(Exception):

    def __init__(self, response):
        msg = '%s, %s' % (response['status_code'], response['status_message'])
        super(RequestError, self).__init__(msg)


def Clei():
    pass

x = 1

def _send_request(request):
    req = urllib.request.Request(
        API_CREATE_MESSAGE_URL,
        json.dumps(request, ensure_ascii=False).encode(),
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def create_message(
    application,
    auth_token,
    content,
    params=None,
    filters=None,
    request_sender=_send_request,
):
    """
    :type application: str
    :type auth_token: str
    :type content: dict[str, str]
    :type params: dict[str, Any]
    :type filters: dict[str, Any]
    :type request_sender: callable
    """
    request = {
        'request': {
            'application': application,
            'auth': auth_token,
            'notifications': [
                _create_notification(content, filters, params),
            ],
        },
    }

    response = request_sender(request)

    if response['status_code'] != 200:
        raise RequestError(response)


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
            op = 'IN'
        else:
            op = 'EQ'
        conditions.append([k, op, v])

    return conditions
