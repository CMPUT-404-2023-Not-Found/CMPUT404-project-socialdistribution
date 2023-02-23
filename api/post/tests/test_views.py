# 2023-02-18
# post/tests.py

from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status

from post.models import Post
from post.views import PostListCreateView

from .base import Base

class PostViewTests(Base):
    '''
    Test suite for Post views
    '''

    '''
    Test Post view GET /authors/uuid/posts
    '''
    def test_list_empty_posts(self):
        '''
        Test no posts
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, []) # type: ignore
    
    def test_list_author_single_post(self):
        '''
        Test one post
        '''
        test_post_data = self.post_model_data
        self.create_post(**test_post_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, [1]) # type: ignore

    def test_list_author_multiple_posts(self):
        '''
        Test multiple posts
        '''
        pass

    def test_get_post_detail(self):
        pass

    def test_update_post(self):
        pass

    def test_create_post_with_id(self):
        pass

    def test_delete_post(self):
        pass

