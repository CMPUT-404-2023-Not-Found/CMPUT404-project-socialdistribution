# 2023-02-18
# post/tests.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from post.models import Post
Author = get_user_model()

class Base(APITestCase):
    '''
    Base class for Post test suite
    '''
    fixtures = ['fixtures/db.json']

    post_data = {
        'unlisted': False,
        'visibility': 'PUBLIC',
        'content': 'Content ' + get_random_string(128),
        'contentType': 'text/plain',
        'description': 'Description ' + get_random_string(32),
        'title': 'Title ' + get_random_string(16)
    }

    def setUp(self):
        self.author = Author.objects.get(username='georgerrmartin')
        self.author_client = self.configure_client(self.author)
        self.admin = Author.objects.get(username='stephenking')
        self.admin_client = self.configure_client(self.admin)
    
    def configure_client(self, user):
        '''
        Return an APIClient authenticated as user
        '''
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
    
    def get_create_post_url(self, author_uuid):
        '''
        Return string http://sitename/authors/author_uuid/posts/
        '''
        return reverse('createPost', kwargs={'author_uuid': str(author_uuid)})
    
    def get_list_post_url(self, author_uuid):
        '''
        Return string http://sitename/authors/author_uuid/posts/
        '''
        return reverse('createPost', kwargs={'author_uuid': str(author_uuid)})

    def get_detail_post_url(self, author_uuid, post_uuid):
        '''
        Return string http://sitename/authors/author_uuid/posts/post_uuid/
        '''
        return reverse('detailPost', kwargs={'author_uuid': str(author_uuid), 'id': str(post_uuid)})
