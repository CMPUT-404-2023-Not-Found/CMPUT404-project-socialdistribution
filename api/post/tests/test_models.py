# 2023-02-18
# post/tests.py

from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from django.contrib.auth import get_user_model
from post.models import Post
from post.views import PostListCreateView

from .base import Base

class PostModelTests(Base):
    '''
    Test suite for Post model
    '''

    '''
    Test Post model POST /authors/uuid/posts
    '''
    def test_create_post(self):
        '''
        Test legit create post
        '''
        test_post_data = self.post_api_data
        response = self.client.post(self.create_post_url, test_post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(test_post_data, response.data) # type: ignore
    
    '''
    Test Post model post.type
    '''
    def test_create_has_type(self):
        pass

    '''
    Test Post model post.title
    '''
    def test_create_with_missing_title(self):
        pass

    def test_create_with_blank_title(self):
        pass

    def test_create_with_long_title(self):
        pass

    def test_create_with_blacklist_title(self):
        pass

    '''
    Test Post model post.id
    '''
    def test_create_id_is_node_id_format(self):
        '''
        Test id node id format: http://sitename/authors/<uuid>/posts/<uuid>
        '''
        pass

    '''
    Test Post model post.source
    '''
    def test_create_with_missing_source(self):
        pass

    def test_create_with_blank_source(self):
        pass

    def test_create_with_long_source(self):
        pass

    def test_create_with_non_url_source(self):
        pass

    def test_create_with_source_of_unknown_node(self):
        pass

    '''
    Test Post model post.origin
    '''
    def test_create_with_missing_origin(self):
        pass

    def test_create_with_blank_origin(self):
        pass

    def test_create_with_long_origin(self):
        pass

    def test_create_with_non_url_origin(self):
        pass

    def test_create_with_origin_of_unknown_node(self):
        pass
    
    '''
    Test Post model post.description
    '''
    def test_create_with_missing_desc(self):
        pass

    def test_create_with_blank_desc(self):
        pass

    def test_create_with_long_desc(self):
        pass

    def test_create_with_blacklist_desc(self):
        pass
    
    '''
    Test Post model post.content_type
    '''
    def test_create_with_content_type_markdown(self):
        pass
    
    def test_create_with_content_type_plaintext(self):
        pass
    
    def test_create_with_content_type_b64(self):
        pass

    def test_create_with_content_type_png(self):
        pass

    def test_create_with_content_type_jpeg(self):
        pass

    def test_create_with_missing_content_type(self):
        pass
    
    def test_create_with_blank_content_type(self):
        pass

    def test_create_with_long_content_type(self):
        pass

    def test_create_with_unknown_content_type(self):
        pass
    
    '''
    Test Post model post.content
    '''
    def test_create_with_missing_content(self):
        pass

    def test_create_with_blank_content(self):
        pass

    def test_create_with_long_content(self):
        pass

    def test_create_with_blacklist_content(self):
        pass

    def test_create_with_content_not_matching_content_type(self):
        pass

    def test_create_with_image_content(self):
        pass
    
    '''
    Test Post model post.author
    '''
    def test_create_has_author_info(self):
        pass

    def test_create_has_only_one_author(self):
        pass

    def test_create_with_missing_author(self):
        pass

    def test_create_with_blank_author(self):
        pass

    def test_create_with_unknown_author(self):
        pass

    def test_create_with_mismatched_authors(self):
        pass

    def test_create_with_non_uuid_author(self):
        pass
    
    '''
    Test Post model post.categories
    '''
    def test_create_with_missing_categories(self):
        pass

    def test_create_with_blank_categories(self):
        pass

    def test_create_with_blacklist_categories(self):
        pass

    def test_create_with_one_category(self):
        pass

    def test_create_with_multiple_categories(self):
        pass

    def test_create_with_too_many_categories(self):
        pass
    
    '''
    Test Post model post.published
    '''
    def test_create_published_is_for_now(self):
        pass

    def test_create_published_datetime_is_iso_format(self):
        '''
        Test published datetime format is ISO-8601 format: 2023-02-23T08:29:43-07:00
        '''
        pass

    '''
    Test Post model post.visibility
    '''
    def test_create_with_missing_visibility(self):
        pass

    def test_create_with_blank_visibility(self):
        pass

    def test_create_with_public_visibility(self):
        pass

    def test_create_with_friends_visibility(self):
        pass

    def test_create_with_unknown_visibility(self):
        pass
    
    '''
    Test Post model post.unlisted
    '''

    def test_create_with_true_unlisted(self):
        pass

    def test_create_with_false_unlisted(self):
        pass

    def test_create_with_missing_unlisted(self):
        pass

    def test_create_with_blank_unlisted(self):
        pass

    def test_create_with_unknown_unlisted(self):
        pass
