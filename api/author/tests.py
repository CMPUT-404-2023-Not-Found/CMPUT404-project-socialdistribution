# 2023-02-15
# author/tests.py

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Author

# This code is modified from a video tutorial from Bobby Stearman on 2022-11-28 retrieved on 2023-02-15, to Youtube freeCodeCamp.org
# video here:
# https://www.youtube.com/watch?v=tujhGdn1EMI
# Module 4: Write unit tests 44:50
class AuthorTestCase(APITestCase):
    '''
    Test suite for Author model
    '''
    def setUp(self):
        self.client = APIClient()
        self.data = { 
            'username': 'testme01',
            'password': 'P*ssw0rd!',
            'host': 'http://localhost:8000'
        }
        self.url = '/api/authors/'
    
    def test_create_author(self):
        '''
        AuthorView: test legit create
        '''
        data = self.data
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().username, data['username'])

    def test_create_author_without_username(self):
        '''
        AuthorView: test when username is not present in data
        '''
        data = self.data
        data.pop("username")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    