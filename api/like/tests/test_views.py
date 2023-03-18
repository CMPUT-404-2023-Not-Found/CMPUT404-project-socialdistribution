# 2023-03-18
# api/like/tests/test_view.py

from django.contrib.auth import get_user_model
from rest_framework import status

from .base import Base

Author = get_user_model()

class LikeListCreateViewTest(Base):
    '''
    Test suite for Author views
    '''
    # from fixtures
    author_uuid = '398113ca-ce82-420a-b1e8-e8de260d3a64'
    post_uuid = 'a0dfc41c-4d32-47d1-a567-aed24ae4736e'
    comment_uuid = 'd18bf964-b9e2-4360-9a5c-1a036bc82db8'
    owner_uuid = 'df396b9e-1815-4f89-9c9f-6e850e00f7c3'
    another_author_uuid = 'ec812fcd-1c90-4080-bf1c-45c3000fb19b'

    # Test Like view /api/authors/<author_uuid>/posts/<post_uuid>/comments/<comment_uuid>/likes
    def test_get_list_of_comment_likes(self):
        '''
        Test getting list of likes on comment
        '''
        response = self.author_client.get(self.get_comment_like_url(self.author_uuid, self.post_uuid, self.comment_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Like view /api/authors/<author_uuid>/posts/<post_uuid>/likes
    def test_get_list_of_post_likes(self):
        '''
        Test getting list of likes on a post
        '''
        response = self.author_client.get(self.get_post_like_url(self.author_uuid, self.post_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_your_own_post_again(self):
        '''
        Test liking your own post again
        '''
        pass

    def test_like_your_own_comment_again(self):
        '''
        Test liking your own comment again
        '''
        pass

    def test_like_another_authors_post(self):
        '''
        Test liking another authors post
        '''
        pass  

    def test_like_another_authors_comment(self):
        '''
        Test liking another authors comment
        '''
        pass
