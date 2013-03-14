from nose.tools import *
import bvapi
import requests

TEST_USER='admin'
TEST_PASSWORD='test'
TEST_URL='http://127.0.0.1:8001/api/v1'
TEST_ACCOUNT_ID=1

def get_client(user=TEST_USER, password=TEST_PASSWORD):
    return bvapi.Client(TEST_URL, user, password)

class Client_test(object):
    def test_client_instantiation(self):
        client = get_client()
        assert client

    @raises(requests.HTTPError)
    def test_client_auth_failure(self):
        client2 = get_client(password='test2')
        client2.status()

    @raises(requests.ConnectionError)
    def test_request_cant_connect(self):
        client = bvapi.Client("http://127.0.0.1:8/api/v1", TEST_USER, TEST_PASSWORD)
        client._request_get('')

class Client2_test(object):
    def setup(self):
        self.client = get_client()

    def teardown(self):
        pass

    def test_client_status(self):
        result = self.client.status()
        eq_(result['status'], 'success')
        eq_(result['version'], 'v1')
        eq_(result['user'], TEST_USER)

    def test_client_account(self):
        result = self.client.account(TEST_ACCOUNT_ID)
        account = result.get('account')
        ok_(account)
        eq_(account.get('id'), TEST_ACCOUNT_ID)

    @raises(bvapi.exceptions.NotFoundError)
    def test_client_account_not_exist(self):
        self.client.account(10000000)

    def test_client_accounts(self):
        result = self.client.accounts()
        accounts = result.get('accounts')
        ok_(accounts)
        ok_(accounts[0]['id'])
