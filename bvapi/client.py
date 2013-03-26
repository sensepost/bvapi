import logging
import requests

from .exceptions import ApiException, NotFoundError

log = logging.getLogger('bvapi.Client')

class Client(object):
    def __init__(self, url, user, password):
        """Constructor for Client class.

        url:      The base url for API access, eg. https://broadviewserver/api/v1
        user:     Username of a valid user with API access.
        password: Password for the specified user.
        """

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
        """Get server status and confirm connectivity/authentication

        Returns:
            current_time -> Server time in ISO 8601 Format including timezone.
            instance_url -> URL for BroadView instance
            version -> Version of the API at that location
            user -> Username of user used in API call
        """

        return self._request_get('')

    def accounts(self):
        """Return a list of all accounts the user can access in desc order.

        Accounts are stored under the 'accounts' key in the returned dict.
        """

        return self._request_get('accounts')

    def jobs(self, account_id):
        """Return a list of all jobs for the specified account_id in desc order.

        Jobs are stored under the 'jobs' key in the returned dict.
        """

        return self._request_get('jobs/%d' % account_id)

    def scans(self, job_id, count=None):
        """Return a list of all scans for the specified job_id in desc order.

        a 'count' can be specified which will control the amount of
        scans returned. The server will enforce a min and max count.

        Scans are stored under the 'scans' key in the returned dict.
        """

        if count:
            return self._request_get('scans/%d/%d' % (job_id, int(count)))
        else:
            return self._request_get('scans/%d' % job_id)

    def scan(self, scan_id):
        """Return the scan for the specified scan_id.

        The scan will be under the 'scan' key, it will also contain all the
        scans issues under the 'issues' key in the scan. Each issue will
        contain extra details related to issue type in under the 'issue_detail'
        key in the issue.
        """

        return self._request_get('scan/%d' % scan_id)
