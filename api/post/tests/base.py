# 2023-02-18
# post/tests.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient, APITestCase

from post.models import Post
Author = get_user_model()

class Base(APITestCase):
    '''
    Base class for Post test suite
    '''
    app_host = 'http://localhost:8000'
    author_data = {
        'username': 'testme00',
        'password': 'P*ssw0rd!',
        'host': app_host
    }

    post_model_data = {
        'unlisted': False,
        'visibility': 'PUBLIC',
        'content': 'Content ' + get_random_string(128),
        'content_type': 'text/plain',
        'description': 'Description ' + get_random_string(32),
        'title': 'Title ' + get_random_string(16)
    }

    post_api_data = {
        'unlisted': False,
        'visibility': 'PUBLIC',
        'content': 'Content ' + get_random_string(128),
        'contentType': 'text/plain',
        'description': 'Description ' + get_random_string(32),
        'title': 'Title ' + get_random_string(16)
    }

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            username = 'testme00',
            password = 'P*ssw0rd!',
            host = self.app_host
        )
        self.author_uuid = str(self.author.id) # type: ignore
        self.create_post_url = reverse('createPost', kwargs={'author_id': self.author_uuid})

    def create_author(self, **author_data):
        return Author.objects.create(**author_data)
    
    def create_post(self, **post_data):
        return Post.objects.create(**post_data)

    def get_author_uuid(self, obj):
        return str(obj.id)
    
    def get_create_post_url(self, obj):
        '''
        Return string http://sitename/authors/author_uuid/posts
        '''
        if obj:
            return reverse('createPost', kwargs={'author': str(obj.id)})
        else:
            return reverse('createPost', kwargs={'author': str(self.author)})
    
    def get_detail_post_url(self, obj, post_uuid):
        '''
        Return string http://sitename/authors/author_uuid/posts/post_uuid
        '''
        if obj:
            return reverse('detailPost', kwargs={'author': str(obj.id), 'id': str(post_uuid)})
        else:
            return reverse('detailPost', kwargs={'author': str(self.author), 'id': str(post_uuid)})
