# 2023-03-15
# follower/tests/test_list_create_view.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .base import Base
from random import choices
import json

Author = get_user_model()

class FollowerListCreateViewTest(Base):
    '''
    Test suite for Follower views
    '''
    # from fixtures
    author_uuid = '398113ca-ce82-420a-b1e8-e8de260d3a64'
    # TODO any way to not hardcode? - Yep, use fixtures
    follower = 'http://localhost:8000/api/authors/664925be-f3ce-42b0-9d34-1659d078f840'
    
    # Test Follower View PUT /api/authors/<author_uuid>/followers/
    def test_put_follower(self):
        '''
        Test creating a follower
        '''
        response = self.author_client.put(self.get_follower_detail_url(self.author_uuid, self.follower))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'success')
    
    # Test Follower view GET /api/authors/<author_uuid>/followers/
    def test_get_list_of_followers(self):
        '''
        Test getting list of followers
        '''
        # response = self.author_client.get(self.get_followers_url(self.author_uuid))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass
    
    # Test Follower view GET /api/authors/<author_uuid>/followers/<follower>/
    def test_get_single_follower(self):
        '''
        Test getting a single follower
        '''
        # response = self.author_client.get(self.get_follower_detail_url(self.author_uuid, self.follower))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        pass

    def test_delete_follower(self):
        '''
        Test deleting a follower from a followee
        '''
        pass
    
