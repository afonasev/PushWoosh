

class RequestError(Exception):

    def __init__(self, response):
        msg = '%s, %s' % (response['status_code'], response['status_message'])
        super(RequestError, self).__init__(msg)
