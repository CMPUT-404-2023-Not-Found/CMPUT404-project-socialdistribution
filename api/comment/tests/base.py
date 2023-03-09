# 2023-03-05
# comments/tests/base.py

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

Author = get_user_model()

class Base(APITestCase):
    '''
    Base class for Author test suite
    '''
    app_host = settings.APP_URL
    fixtures = ['fixtures/db.json']

    def setUp(self):
        self.author = Author.objects.get(username='georgerrmartin')
        self.admin = Author.objects.get(username='stephenking')
        self.another_author = Author.objects.get(username='edgarallanpoe')
        self.author_client = self.configure_client(self.author)
        self.admin_client = self.configure_client(self.admin)

    def configure_client(self, user):
        '''
        Return an APIClient authenticated as user
        '''
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
    
    def get_comment_url(self, author_uuid, post_uuid):
        '''
        Return string http://sitename/authors/<author_uuid>/posts/<post_uuid>/comments
        '''
        return reverse('comment', kwargs={'author_uuid': str(author_uuid), 'post_uuid': str(post_uuid)})
    
    def get_comment_detail_url(self, author_uuid, post_uuid, uuid):
        '''
        Return string http://sitename/authors/<author_uuid>/
        '''
        return reverse('detailComment', kwargs={'author_uuid': str(author_uuid), 'post_uuid': str(post_uuid), 'id': str(uuid)})


