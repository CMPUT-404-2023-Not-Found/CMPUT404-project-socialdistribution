# 2023-02-18
# post/tests.py

from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from django.contrib.auth import get_user_model
from post.models import Post
from post.views import PostListCreateView

Author = get_user_model()

class PostTests(APITestCase):
    '''
    Test suite for Post model
    '''
    def setUp(self):
        self.client = APIClient()

        self.app_host = 'http://localhost:8000'
        self.author = Author.objects.create(
            username = 'testme00',
            password = 'P*ssw0rd!',
            host = self.app_host
        )
        self.author_uuid = str(self.author.id) # type: ignore
        self.url = reverse('createPost', kwargs={'author_id': self.author_uuid})

    def test_list_empty_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, []) # type: ignore
    
    def test_create_post(self):
        test_post_data = {
            'host': self.app_host,
            'unlisted': False,
            'visibility': 'PUBLIC',
            'origin': self.app_host,
            'source': self.app_host,
            'content': 'Content: ' + get_random_string(128),
            'contentType': 'text/plain',
            'description': 'Description: ' + get_random_string(32),
            'title': 'Title: ' + get_random_string(16)
        }
        response = self.client.post(self.url, test_post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_author_single_post(self):
        pass

    def test_list_author_multiple_posts(self):
        pass

    def test_get_post_detail(self):
        pass

    def test_update_post(self):
        pass

    def test_create_post_with_id(self):
        pass

    def test_delete_post(self):
        pass

