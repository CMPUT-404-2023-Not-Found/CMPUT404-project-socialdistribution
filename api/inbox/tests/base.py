# 2023-02-26
# inbox/tests/base.py

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

Author = get_user_model()

class Base(APITestCase):
    '''
    Base class for Inbox test suite
    '''
    app_host = settings.APP_URL
    fixtures = ['fixtures/db.json', 'fixtures/small.json']
    # fixtures/db.json values
    admin_username = 'stephenking'
    # fixtures/small.json values
    first_author_username = 'jrrtolkien'
    second_author_username = 'jkrowling'
    second_author_public_post_node_id = 'http://localhost:8000/api/authors/80e83b86-0d26-4189-b68a-bf57e8c87af1/posts/6587d10f-e435-48b3-ab3e-30bae3b800fb/'

    def setUp(self):
        self.admin = Author.objects.get(username=self.admin_username)
        self.first_author = Author.objects.get(username=self.first_author_username)
        self.second_author = Author.objects.get(username=self.second_author_username)
        self.author_client = self.configure_client(self.first_author)
        self.admin_client = self.configure_client(self.admin)

    def configure_client(self, user):
        '''
        Return an APIClient authenticated as user
        '''
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
    
    def get_inbox_url(self, uuid):
        '''
        Return string http://sitename/authors/<author_uuid>/inbox/
        '''
        return reverse('inbox', kwargs={'author_uuid': str(uuid)})
