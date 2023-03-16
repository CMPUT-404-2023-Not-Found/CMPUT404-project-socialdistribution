# 2023-03-15
# follower/tests/test_list_create_view.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from random import choices
import json
import logging

from .base import Base
from follower.serializers import FollowerSerializer

Author = get_user_model()
logger = logging.getLogger('django')
rev = 'rev: $jsadasd'

class FollowerListCreateViewTest(Base):
    '''
    Test suite for Follower views
    '''
    # from fixtures
    author_uuid = '398113ca-ce82-420a-b1e8-e8de260d3a64'
    # TODO any way to not hardcode? - Yep, use fixtures/fucntions
    follower = 'http://localhost:8000/api/authors/664925be-f3ce-42b0-9d34-1659d078f840'
    
    def create_follower(self, follower):
        '''
        Create a follower
        '''
        return self.author_client.put(self.get_follower_detail_url(self.author_uuid, follower))

    
    # Test Follower View PUT /api/authors/<author_uuid>/followers/
    def test_put_follower(self):
        '''
        Test creating a follower
        '''
        response = self.create_follower(self.follower)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], self.follower)
    
    # Test Follower view GET /api/authors/<author_uuid>/followers/
    def test_get_list_of_followers(self):
        '''
        Test getting list of followers
        '''
        # response = self.author_client.put(self.get_follower_detail_url(self.author_uuid, self.follower))
        response = self.create_follower(self.follower)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.author_client.get(self.get_followers_url(self.author_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)

    # Test Follower view GET /api/authors/<author_uuid>/followers/<follower>/
    def test_get_single_follower(self):
        '''
        Test getting a single follower
        '''
        # response = self.author_client.put(self.get_follower_detail_url(self.author_uuid, self.follower))
        response = self.create_follower(self.follower)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
        response = self.author_client.get(self.get_follower_detail_url(self.author_uuid, self.follower))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_follower(self):
        '''
        Test deleting a follower from a followee
        '''
        # response = self.author_client.put(self.get_follower_detail_url(self.author_uuid, self.follower))
        response = self.create_follower(self.follower)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
        response = self.author_client.delete(self.get_follower_detail_url(self.author_uuid, self.follower))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.author_client.get(self.get_follower_detail_url(self.author_uuid, self.follower))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
