# 2023-02-26
# comment/tests/test_list_create_view.py

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

class LikeListCreateViewTest(Base):
    '''
    Test suite for Author views
    '''
    # from fixtures
    author_uuid = '398113ca-ce82-420a-b1e8-e8de260d3a64'
    post_uuid = 'a0dfc41c-4d32-47d1-a567-aed24ae4736e'
    comment_uuid = 'd18bf964-b9e2-4360-9a5c-1a036bc82db8'
    owner_uuid = 'df396b9e-1815-4f89-9c9f-6e850e00f7c3'
    another_author_uuid = 'ec812fcd-1c90-4080-bf1c-45c3000fb19b'

    # Test Like view GET /api/authors/<author_uuid>/posts/<post_uuid>/comments/<comment_uuid>/likes
    def test_get_list_of_comment_likes(self):
        '''
        Test getting list of likes on comment
        '''
        response = self.admin_client.get(self.get_comment_like_url(self.author_uuid, self.post_uuid, self.comment_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Like view GET /api/authors/<author_uuid>/posts/<post_uuid>/likes
    def test_get_list_of_post_likes(self):
        '''
        Test getting list of likes on a post
        '''
        response = self.admin_client.get(self.get_post_like_url(self.author_uuid, self.post_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test Like detail view GET /api/authors/<author_uuid>/posts/<post_uuid>/comments/<comment_uuid>/likes/<owner_uuid>
    def test_get_single_comment_like(self):
        '''
        Test getting a single like on a comment
        '''
        response = self.admin_client.get(self.get_comment_like_detail_url(self.author_uuid, self.post_uuid, self.comment_uuid, self.another_author_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Like detail view GET /api/authors/<author_uuid>/posts/<post_uuid>/comments/<comment_uuid>/likes/<owner_uuid>
    def test_get_single_post_like(self):
        '''
        Test getting a single like on a post
        '''
        response = self.admin_client.get(self.get_post_like_detail_url(self.author_uuid, self.post_uuid, self.another_author_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Like View POST authors/<author_uuid>/posts/<post_uuid>/likes/
    def test_like_your_own_post_again(self):
        '''
        Test liking your own post again
        '''
        body = {
            "context": "https://www.w3.org/ns/activitystreams"
        }
        response = self.author_client.post(self.get_post_like_url(self.author_uuid, self.post_uuid), body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Like View POST authors/<author_uuid>/posts/<post_uuid>/comments/<comment_uuid>/likes
    def test_like_your_own_comment_again(self):
        '''
        Test liking your own comment again
        '''
        body = {
            "context": "https://www.w3.org/ns/activitystreams"
        }
        response = self.author_client.post(self.get_comment_like_url(self.author_uuid, self.post_uuid, self.comment_uuid), body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Like View POST authors/<author_uuid>/posts/<post_uuid>/likes/
    def test_like_another_authors_post(self):
        '''
        Test liking another authors post
        '''
        body = {
            "context": "https://www.w3.org/ns/activitystreams"
        }
        response = self.like_owner_client.post(self.get_post_like_url(self.author_uuid, self.post_uuid), body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)     

    # Test Like View POST authors/<author_uuid>/posts/<post_uuid>/comments/<comment_uuid>/likes/
    def test_like_another_authors_comment(self):
        '''
        Test liking another authors comment
        '''
        body = {
            "context": "https://www.w3.org/ns/activitystreams"
        }
        response = self.like_owner_client.post(self.get_comment_like_url(self.author_uuid, self.post_uuid, self.comment_uuid), body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)