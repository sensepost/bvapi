from nose.tools import *
import bvapi

def get_client(user='test', password='test'):
    return bvapi.Client("http://127.0.0.1:8001/api/v1", user, password)

class Client_test(object):
    def test_client_instantiation(self):
        client = get_client()
        assert client


class Client2_test(object):
    def setup(self):
        self.client = get_client()

    def teardown(self):
        pass

"""
    @raises(bvapi.exceptions.ConnectionError)
    def test_request_cant_connect(self):
        self.client._request_get('')

    def test_client_status(self):
        result = self.client.status()
        eq_(result['status'], 'success')
        eq_(result['version'], 'v1')

    def test_client_auth_failure(self):
        client2 = get_client(password='test2')
        result = client2.status()
        eq_(result['status'], 'error')
        eq_(result['error'], 'authentication failure')
        """
