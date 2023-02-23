# 2023-02-18
# post/tests.py

from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status

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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, []) # type: ignore
    
    def test_list_single_post(self):
        '''
        Test one post
        '''
        test_post_data = self.post_model_data
        self.create_post(**test_post_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, [1]) # type: ignore

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
        pass
    
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
        pass

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
        pass

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

