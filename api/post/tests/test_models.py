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

    def test_create_with_long_title(self):
        pass

    def test_create_with_blacklist_title(self):
        pass
    
    def test_create_with_missing_source(self):
        pass

    def test_create_with_blank_source(self):
        pass

    def test_create_with_long_source(self):
        pass

    def test_create_with_non_url_source(self):
        pass

    def test_create_with_source_of_unknown_node(self):
        pass

    def test_create_with_missing_origin(self):
        pass

    def test_create_with_blank_origin(self):
        pass

    def test_create_with_long_origin(self):
        pass

    def test_create_with_non_url_origin(self):
        pass

    def test_create_with_origin_of_unknown_node(self):
        pass
    
    def test_create_with_missing_desc(self):
        pass

    def test_create_with_blank_desc(self):
        pass

    def test_create_with_long_desc(self):
        pass

    def test_create_with_blacklist_desc(self):
        pass

    def test_create_with_missing_contenttype(self):
        pass

    def test_create_with_blank_contenttype(self):
        pass

    def test_create_with_long_contenttype(self):
        pass

    def test_create_with_unknown_contenttype(self):
        pass

    def test_create_with_missing_content(self):
        pass

    def test_create_with_blank_content(self):
        pass

    def test_create_with_long_content(self):
        pass

    def test_create_with_blacklist_content(self):
        pass

    def test_create_with_missing_author(self):
        pass

    def test_create_with_blank_author(self):
        pass

    def test_create_with_unknown_author(self):
        pass

    def test_create_with_mismatched_authors(self):
        pass

    def test_create_with_non_uuid_author(self):
        pass

    def test_create_with_missing_categories(self):
        pass

    def test_create_with_blank_categories(self):
        pass

    def test_create_with_blacklist_categories(self):
        pass

    def test_create_with_one_category(self):
        pass

    def test_create_with_multiple_categories(self):
        pass

    def test_create_with_missing_visibility(self):
        pass

    def test_create_with_blank_visibility(self):
        pass

    def test_create_with_public_visibility(self):
        pass

    def test_create_with_friends_visibility(self):
        pass

    def test_create_with_unknown_visibility(self):
        pass
    
    def test_create_with_missing_unlisted(self):
        pass

    def test_create_with_blank_unlisted(self):
        pass

    def test_create_with_unknown_unlisted(self):
        pass
