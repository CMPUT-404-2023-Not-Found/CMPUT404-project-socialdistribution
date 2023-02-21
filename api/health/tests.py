# 2023-02-20
# health/test.py

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class HealthTestCase(APITestCase):
    '''
    Simple Test Suite for the health app
    '''
    def setUp(self):
        self.client = APIClient()
        self.url = '/health/'
    
    def test_version_check(self):
        '''
        Test that the version.txt endpoint is reachable
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that response contains something similiar to what is found in api/health/ver.txt
        self.assertRegex(list(response.streaming_content)[0].decode(), '^SD [a-zA-Z0-9 -:]+ PR[0-9]+$') # type: ignore
