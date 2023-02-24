# 2023-02-24
# authentication/tests.py

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class AuthenticationTests(APITestCase):
    '''
    Authentication test suite
    '''
    app_host = settings.APP_URL
    fixtures = ['fixtures/db.json']

    def setUp(self):
        self.client = APIClient()
        self.inactive_author = {'username':'edgarallenpoe', 'password':'P*ssw0rd!'}
        self.active_author = {'username':'georgerrmartin', 'password':'P*ssw0rd!'}
        self.login_url = reverse('token_obtain_pair')
        self.refresh_token_url = reverse('token_refresh')
        self.verify_token_url = reverse('token_verify')
    
    '''
    Test Authentication view /api/token/
    '''
    def test_login(self):
        '''
        Test legit login
        '''
        test_login_data = self.active_author
        response = self.client.post(self.login_url, test_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data) # type: ignore
        self.assertTrue('access' in response.data) # type: ignore
    
    def test_login_with_missing_password(self):
        '''
        Test login with a missing password payload
        '''
        test_login_data = self.active_author
        test_login_data.pop('password')
        response = self.client.post(self.login_url, test_login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse('refresh' in response.data) # type: ignore
        self.assertFalse('access' in response.data) # type: ignore

    def test_login_with_blank_password(self):
        '''
        Test login with a blank password payload
        '''
        test_login_data = self.active_author
        test_login_data['password'] = ''
        response = self.client.post(self.login_url, test_login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse('refresh' in response.data) # type: ignore
        self.assertFalse('access' in response.data) # type: ignore

    def test_login_with_missmatched_password(self):
        '''
        Test login with a missmatched password
        '''
        test_login_data = self.active_author
        test_login_data['password'] = get_random_string(16)
        response = self.client.post(self.login_url, test_login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('refresh' in response.data) # type: ignore
        self.assertFalse('access' in response.data) # type: ignore

    def test_login_with_inactive_author(self):
        '''
        Test login with an inactive author
        '''
        test_login_data = self.inactive_author
        response = self.client.post(self.login_url, test_login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('refresh' in response.data) # type: ignore
        self.assertFalse('access' in response.data) # type: ignore

    '''
    Test Authentication view /api/token/refresh/
    '''
    def test_refresh_token(self):
        pass

    '''
    Test Authentication view /api/token/verify/
    '''
    def test_verify_token(self):
        pass
