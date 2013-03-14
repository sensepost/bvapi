import logging
import requests

from .exceptions import ApiException, NotFoundError

log = logging.getLogger('bvapi.Client')

class Client(object):
    def __init__(self, url, user, password):
        if not url.endswith('/'):
            url += '/'
        self.url = url
        self.user = user
        self.password = password

    def _request_get(self, path):
        res = requests.get(self.url + path, auth=(self.user, self.password))

        res.raise_for_status()
        data = res.json()

        if data.get('status') == 'success':
            return data
        elif data.get('status') == 'error':
            if data.get('error_type') == 'no such object':
                raise NotFoundError(data.get('error_msg'))
            else:
                raise ApiException(data)
        else:
            raise ApiException(data)

    def status(self):
        return self._request_get('')

    def account(self, account_id):
        return self._request_get('account/%d' % account_id)

    def accounts(self):
        return self._request_get('accounts')
