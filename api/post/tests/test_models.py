# 2023-02-18
# post/tests.py

from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from django.contrib.auth import get_user_model
from post.models import Post
from post.views import PostListCreateView

from .base import Base

class PostModelTests(Base):
    '''
    Test suite for Post views
    '''

    '''
    Test Post model POST /authors/uuid/posts
    '''
    def test_create_post(self):
        '''
        Test legit create post
        '''
        test_post_data = self.post_api_data
        response = self.client.post(self.url, test_post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(test_post_data, response.data) # type: ignore
    
    def test_create_with_missing_title(self):
        pass

    def test_create_with_blank_title(self):
        pass
