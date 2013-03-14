import logging
import requests
try:
    import simplejson as json
except ImportError:
    import json

class Client(object):
    def __init__(self, url, user, password):
        if not url.endswith('/'):
            url += '/'
        self.url = url
        self.user = user
        self.password = password

    def _request_get(self, path):
        res = requests.get(self.url + path)
        return json.loads(res.content)

    def status(self):
        return self._request_get('')
