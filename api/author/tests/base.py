# 2023-02-18
# author/base.py

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient, APITestCase

Author = get_user_model()

class Base(APITestCase):
    '''
    Base class for Author test suite
    '''
    app_host = settings.APP_URL
    fixtures = ['fixtures/db.json']
    author_data = {
        'username': 'testme00',
        'password': 'P*ssw0rd!',
        'host': app_host
    }

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            username = 'testme00',
            password = 'P*ssw0rd!',
            host = self.app_host
        )
        self.author_uuid = str(self.author.id)

    def get_author_uuid(self, obj):
        return str(obj.id)
    
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
