import datetime
from nose.tools import *
import requests

import bvapi
import dateutil.parser

TEST_USER='admin'
TEST_PASSWORD='test'
TEST_URL='http://127.0.0.1:8001/api/v1'
TEST_ACCOUNT_ID=1
TEST_JOB_ID=1
TEST_SCAN_ID=1

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
        dt = dateutil.parser.parse(result['current_time'])
        ok_(dt.tzinfo)

    def test_client_accounts(self):
        result = self.client.accounts()
        accounts = result.get('accounts')
        ok_(accounts)
        ok_(accounts[0]['id'])

    def test_client_jobs(self):
        result = self.client.jobs(TEST_ACCOUNT_ID)
        jobs = result.get('jobs')
        ok_(jobs)
        ok_(jobs[0].get('id'))

    @raises(bvapi.exceptions.NotFoundError)
    def test_client_jobs_not_exist(self):
        self.client.jobs(10000000)

    def test_client_scans(self):
        result = self.client.scans(TEST_JOB_ID)
        scans = result.get('scans')
        ok_(scans)
        ok_(scans[0].get('id'))

    @raises(bvapi.exceptions.NotFoundError)
    def test_client_scan_not_exist(self):
        self.client.scan_data(10000000)

    def test_client_scan_data(self):
        result = self.client.scan_data(TEST_SCAN_ID)
        scan = result.get('scan')
        ok_(scan)
        ok_(scan.get('id'))
        ok_('issues' in scan)
