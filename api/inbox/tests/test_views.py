# 2023-02-26
# author/tests/test_views.py

from rest_framework import status

from .base import Base
from inbox.models import Inbox

class InboxViewTests(Base):
    '''
    Test suite for Inbox views
    '''

    # Test Inbox view GET /api/authors/uuid/inbox
    def test_get_inbox(self):
        '''
        Test getting an inbox of an author 
        '''
        inbox_count = Inbox.objects.filter(author=self.first_author.id).count()
        response = self.author_client.get(self.get_inbox_url(self.first_author.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], inbox_count)
    
    # Test Inbox view POST /api/authors/uuid/
    def test_add_post_to_first_authors_inbox(self):
        '''
        Test adding a post to an author's inbox
        '''
        test_inbox_data = {'@context': 'https://www.w3.org/ns/activitystreams',
                            'summary': 'Shared post',
                            'type': 'post',
                            'author': self.serialize_author(self.second_author),
                            'object': self.second_author_public_post_node_id
                        }
        response = self.author_client.post(self.get_inbox_url(self.first_author.id), test_inbox_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # Test Inbox view DELETE /api/authors/uuid/
    def test_delete_first_authors_inbox(self):
        '''
        Test deleting an author's inbox
        '''
        response = self.author_client.delete(self.get_inbox_url(self.first_author.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        inbox_count = Inbox.objects.filter(author=self.first_author.id).count()
        self.assertEqual(inbox_count, 0)
