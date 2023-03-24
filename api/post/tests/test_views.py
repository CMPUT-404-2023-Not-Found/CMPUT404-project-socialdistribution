# 2023-02-18
# post/tests.py

from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
import uuid

from post.models import Post
from post.views import PostListCreateView

from .base import Base

class PostViewTests(Base):
    '''
    Test suite for Post views
    '''

    '''
    Test Post view GET /authors/uuid/posts
    '''
    def test_list_empty_posts(self):
        '''
        Test no posts
        '''
        list_post_url = self.get_list_post_url(self.admin.id)
        response = self.admin_client.get(list_post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items'], [])
    
    def test_list_single_post(self):
        '''
        Test one post
        '''
        create_post_url = self.get_create_post_url(self.friendlybaker.id)
        list_response = self.author_client.get(create_post_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data['items']), 1)

    def test_list_post_as_friend(self):
        '''
        Test friend posts
        '''
        create_post_url = self.get_create_post_url(self.author.id)
        list_response = self.friendlybaker_client.get(create_post_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data['items']), 2)


    def test_list_post_as_stranger(self):
        '''
        Test friend posts
        '''
        create_post_url = self.get_create_post_url(self.author.id)
        list_response = self.clarence0_client.get(create_post_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data['items']), 1)

    def test_list_multiple_posts(self):
        '''
        Test multiple posts
        '''
        pass
    
    def test_list_too_many_posts(self):
        pass
    
    def test_list_with_unknown_author(self):
        pass

    def test_list_with_bad_author_uuid(self):
        pass

    '''
    Test Post view GET /authors/uuid/posts/?page=x&size=y
    '''
    def test_list_with_zero_page(self):
        pass

    def test_list_with_one_page(self):
        pass

    def test_list_with_multiple_page(self):
        pass

    def test_list_with_max_pages(self):
        pass

    def test_list_with_bad_page_value(self):
        pass

    def test_list_with_blank_page_value(self):
        pass

    def test_list_with_zero_page_size(self):
        pass
    
    def test_list_with_one_page_size(self):
        pass
    
    def test_list_with_multiple_page_size(self):
        pass
    
    def test_list_with_max_page_size(self):
        pass

    def test_list_with_bad_page_size_value(self):
        pass
    
    def test_list_with_reverse_query(self):
        '''
        Test with query params in reverse order
        '''
        pass

    '''
    Test Post view GET /authors/uuid/posts/uuid
    '''
    def test_get_post_detail(self):
        detail_post_url = self.get_detail_post_url(self.author.id, self.author_post_uuid)
        detail_response = self.author_client.get(detail_post_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

        expect_post_node_id = f'{self.author.get_node_id()}/posts/{self.author_post_uuid}'
        self.assertEqual(detail_response.data['id'], expect_post_node_id)
    
    def test_get_public_post_as_stranger(self):
        detail_post_url = self.get_detail_post_url(self.author.id, self.author_post_uuid)     
        detail_response = self.clarence0_client.get(detail_post_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

    def test_get_friend_post_as_a_friend(self):
        friend_post_url = self.get_detail_post_url(self.author.id, self.friend_post_uuid) 
        detail_response = self.friendlybaker_client.get(friend_post_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

    def test_get_friend_post_as_a_stranger(self):
        friend_post_url = self.get_detail_post_url(self.author.id, self.friend_post_uuid) 
        detail_response = self.clarence0_client.get(friend_post_url)
        self.assertEqual(detail_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_unlisted_post(self):
        pass

    def test_get_post_without_author_uuid(self):
        pass

    def test_get_post_with_bad_author_uuid(self):
        pass

    def test_get_post_with_unknown_author_uuid(self):
        pass

    def test_get_post_without_post_uuid(self):
        pass

    def test_get_post_with_bad_post_uuid(self):
        pass

    def test_get_post_with_unknown_post_uuid(self):
        pass
    
    '''
    Test Post view POST /authors/uuid/posts/uuid
    '''
    def test_update_post(self):
        detail_post_url = self.get_detail_post_url(self.author.id, self.author_post_uuid)
        test_post_data = self.post_data
        detail_response = self.author_client.post(detail_post_url, data=test_post_data)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
    
    def test_update_post_without_author_uuid(self):
        pass

    def test_update_post_with_bad_author_uuid(self):
        pass

    def test_update_post_with_unknown_author_uuid(self):
        pass
    
    def test_update_post_with_missmatched_author_uuid(self):
        pass

    def test_update_post_without_post_uuid(self):
        pass

    def test_update_post_with_bad_post_uuid(self):
        pass

    def test_update_post_with_unknown_post_uuid(self):
        pass

    def test_update_post_with_missmatched_post_uuid(self):
        pass
    
    '''
    Test Post view PUT /authors/uuid/posts/uuid
    '''
    def test_put_post_with_id(self):
        test_post_uuid = str(uuid.uuid4())
        detail_post_url = self.get_detail_post_url(self.author.id, test_post_uuid)
        test_post_data = self.post_data
        test_post_data['description'] = 'test'
        detail_response = self.author_client.put(detail_post_url, data=test_post_data)
        self.assertEqual(detail_response.status_code, status.HTTP_201_CREATED)
        expect_post_node_id = f'{self.author.get_node_id()}/posts/{test_post_uuid}'
        self.assertEqual(detail_response.data['id'], expect_post_node_id)

    def test_put_post_without_author_uuid(self):
        pass

    def test_put_post_with_bad_author_uuid(self):
        pass

    def test_put_post_with_unknown_author_uuid(self):
        pass

    def test_put_post_with_missmatched_author_uuid(self):
        pass

    def test_put_post_without_post_uuid(self):
        pass

    def test_put_post_with_bad_post_uuid(self):
        pass

    def test_put_post_with_unknown_post_uuid(self):
        pass

    def test_put_post_with_missmatched_post_uuid(self):
        pass
    
    '''
    Test Post view DELETE /authors/uuid/posts/uuid
    '''
    def test_delete_post(self):
        detail_post_url = self.get_detail_post_url(self.author.id, self.author_post_uuid)
        detail_response = self.author_client.delete(detail_post_url)
        self.assertEqual(detail_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_without_author_uuid(self):
        pass

    def test_delete_post_with_bad_author_uuid(self):
        pass

    def test_delete_post_with_unknown_author_uuid(self):
        pass

    def test_delete_post_with_missmatched_author_uuid(self):
        pass

    def test_delete_post_without_post_uuid(self):
        pass

    def test_delete_post_with_bad_post_uuid(self):
        pass

    def test_delete_post_with_unknown_post_uuid(self):
        pass

    def test_delete_post_with_missmatched_post_uuid(self):
        pass

