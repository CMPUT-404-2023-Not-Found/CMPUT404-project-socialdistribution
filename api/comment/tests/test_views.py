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

class CommentListCreateViewTest(Base):
    '''
    Test suite for Author views
    '''
    # from fixtures
    author_uuid = '398113ca-ce82-420a-b1e8-e8de260d3a64'
    post_uuid = 'a0dfc41c-4d32-47d1-a567-aed24ae4736e'
    comment_uuid = '1bc05dee-7f18-426d-9f89-989bea9c49c5'

    # Test Comment view GET /api/authors/<author_uuid>/posts/<post_uuid>/comments
    def test_get_list_of_comments(self):
        '''
        Test getting list of comments
        '''
        response = self.admin_client.get(self.get_comment_url(self.author_uuid, self.post_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test Comment view GET /api/authors/<author_uuid>/posts/<post_uuid>/comments/<comment_uuid>
    def test_get_single_comment(self):
        '''
        Test getting a single comment
        '''
        response = self.admin_client.get(self.get_comment_detail_url(self.author_uuid, self.post_uuid, self.comment_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test Comment View POST authors/<author_uuid>/posts/<post_uuid>/comments/
    def test_post_comment(self):
        '''
        Test creating a comment
        '''
        alphanum = "ABCDEFGHIJKLMONOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"
        rand = ''.join(choices(alphanum, k=8))
        body = {
        "comment" : f"{rand} Content",
        "contentType": "text/plain"
        }
        response = self.author_client.post(self.get_comment_url(self.author_uuid, self.post_uuid), body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # Test Comment View pagination
    def test_pagination(self):
        '''
        Test getting a comment from a paginated list
        '''
        comment_url = self.get_comment_url(self.author_uuid, self.post_uuid)
        paginated_url = comment_url + '?page=3&size=1'
        response = self.admin_client.get(paginated_url)
        # get the only comment on the third page, must be the oldest comment
        self.assertEqual(response.json()['comments'][0]['comment'], 'hello')
        self.assertEqual(len(response.json()['comments']), 1)