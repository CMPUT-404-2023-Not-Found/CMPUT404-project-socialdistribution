# 2023-02-26
# author/tests/test_views.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .base import Base

Author = get_user_model()

class AuthorViewTests(Base):
    '''
    Test suite for Author views
    '''

    # Test Author view GET /api/authors/
    def test_get_list_of_authors(self):
        '''
        Test getting list of authors
        '''
        response = self.admin_client.get(self.get_author_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_list_of_authors_without_permissions(self):
        '''
        Test getting list of authors with non-admin permissions
        '''
        response = self.author_client.get(self.get_author_url())
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_list_of_authors_as_anonymous_user(self):
        '''
        Test getting list of authors as anonymous user
        '''
        c = APIClient()
        response = c.get(self.get_author_url())
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test Author view GET /api/authors/uuid/
    def test_get_author_profile(self):
        '''
        Test getting own self's author profile
        '''
        response = self.author_client.get(self.get_author_detail_url(str(self.author.id)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.author.get_node_id())

    def test_get_anothers_author_profile(self):
        '''
        Test getting another author's profile
        '''
        response = self.author_client.get(self.get_author_detail_url(str(self.another_author.id)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.another_author.get_node_id())

    def test_get_author_with_auth_basic(self):
        '''
        Test getting another author's profile with http basic
        '''
        c = self.configure_client(user=self.basic_auth_author, auth_type='Basic')
        response = c.get(self.get_author_detail_url(str(self.another_author.id)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.another_author.get_node_id())
    
    # Test Author view POST /api/authors/uuid/
    def test_update_author_profile(self):
        '''
        Test updating own self's author profile
        '''
        test_author_data = {'displayName': 'test'}
        response = self.author_client.post(self.get_author_detail_url(str(self.author.id)), test_author_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['displayName'], 'test')

        new_author_profile = Author.objects.get(username=self.author.get_username())
        self.assertEqual(new_author_profile.display_name, 'test')
    
    def test_update_another_authors_profile(self):
        '''
        Test updating another author's profile
        '''
        test_author_data = {'displayName': 'test'}
        response = self.author_client.post(self.get_author_detail_url(str(self.another_author.id)), test_author_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        another_author_profile = Author.objects.get(username=self.another_author.get_username())
        self.assertNotEqual(another_author_profile.display_name, 'test')

    def test_update_authors_username(self):
        '''
        Test updating an author's username
        '''
        test_author_data = {'username': 'testme01'}
        response = self.author_client.post(self.get_author_detail_url(str(self.another_author.id)), test_author_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        author_profile = Author.objects.get(username=self.author.get_username())
        self.assertNotEqual(author_profile.get_username, 'testme01')
        
