# 2023-02-26
# author/tests/base.py

import base64
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
    fixture_password = 'P*ssw0rd!' # All fixture author accounts have the same password

    def setUp(self):
        self.author = Author.objects.get(username='georgerrmartin')
        self.admin = Author.objects.get(username='stephenking')
        self.another_author = Author.objects.get(username='edgarallanpoe')
        self.author_client = self.configure_client(self.author)
        self.admin_client = self.configure_client(self.admin)

    def configure_client(self, user, password='P*ssw0rd!', auth_type='Bearer'):
        '''
        Return an APIClient authenticated as user model
        '''
        client = APIClient()
        if auth_type == 'Bearer':
            refresh = RefreshToken.for_user(user)
            client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        else:
            login_cred = f'{user.username}:{password}'
            login_cred_b64 = base64.b64encode(login_cred.encode('ascii')).decode('ascii')
            client.credentials(HTTP_AUTHORIZATION=f'Basic {login_cred_b64}')
        return client
    
    def get_author_url(self):
        '''
        Return string http://sitename/authors/
        '''
        return reverse('author')
    
    def get_author_detail_url(self, uuid):
        '''
        Return string http://sitename/authors/<author_uuid>/
        '''
        return reverse('authorDetail', kwargs={'id': str(uuid)})
