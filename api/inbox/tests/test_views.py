# 2023-02-26
# author/tests/test_views.py

from rest_framework import status
from rest_framework.test import APIClient
from .base import Base

class InboxViewTests(Base):
    '''
    Test suite for Inbox views
    '''

    # Test Inbox view GET /api/authors/uuid/inbox
    def test_get_inbox(self):
        '''
        Test getting an inbox of an author 
        '''
        response = self.author_client.get(self.get_inbox_url(self.first_author.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test Inbox view POST /api/authors/uuid/
    def test_add_post_to_first_authors_inbox(self):
        '''
        Test adding a post to an author's inbox
        '''
        test_inbox_data = {'@context': 'https://www.w3.org/ns/activitystreams',
                            'summary': 'Shared post',
                            'type': 'post',
                            'author': self.second_author.get_node_id(),
                            'object': self.second_author_public_post_node_id
                        }
        response = self.author_client.post(self.get_inbox_url(self.first_author.id), test_inbox_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # Test Inbox view DELETE /api/authors/uuid/
    def test_delete_first_authors_inbox(self):
        '''
        Test deleting an author's inbox
        '''
        response = self.author_client.delete(self.get_inbox_url(self.first_author.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
