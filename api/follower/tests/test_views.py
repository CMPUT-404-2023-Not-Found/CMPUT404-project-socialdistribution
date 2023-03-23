# 2023-03-15
# follower/tests/test_list_create_view.py

from django.contrib.auth import get_user_model
from rest_framework import status
import logging

from .base import Base

Author = get_user_model()
logger = logging.getLogger('django')
rev = 'rev: $jsadasd'

class FollowerListCreateViewTest(Base):
    '''
    Test suite for Follower views
    '''
    author_uuid      = '398113ca-ce82-420a-b1e8-e8de260d3a64'
    follower         = 'http://localhost:8000/api/authors/664925be-f3ce-42b0-9d34-1659d078f840'
    another_follower = 'http://localhost:8000/api/authors/de52020f-f5df-4361-b771-2829a99f16a2'

    # Test Follower View PUT /api/authors/<author_uuid>/followers/
    def test_put_follower(self):
        '''
        Test creating a follower
        '''
        response = self.author_client.put(self.get_follower_detail_url(self.author_uuid, self.follower))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["follower_node_id"], self.follower)
    
    # Test Follower view GET /api/authors/<author_uuid>/followers/
    def test_get_list_of_followers(self):
        '''
        Test getting list of followers
        '''
        response = self.author_client.get(self.get_followers_url(self.author_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)

    # Test Follower view GET /api/authors/<author_uuid>/followers/<follower>/
    def test_get_single_follower(self):
        '''
        Test getting a single follower
        '''
        response = self.author_client.get(self.get_follower_detail_url(self.author_uuid, self.another_follower))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_follower(self):
        '''
        Test deleting a follower from a followee
        '''
        response = self.author_client.delete(self.get_follower_detail_url(self.author_uuid, self.another_follower))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        response = self.author_client.get(self.get_follower_detail_url(self.author_uuid, self.another_follower))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
