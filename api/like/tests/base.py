# 2023-03-05
# comments/tests/base.py

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.management import call_command


Author = get_user_model()

class Base(APITestCase):
    '''
    Base class for Author test suite
    '''
    app_host = settings.APP_URL
    fixtures = ['fixtures/authors.json', 'fixtures/posts.json', 'fixtures/comments.json', 'fixtures/likes.json']
    def setUp(self):
        self.author = Author.objects.get(username='georgerrmartin')
        self.admin = Author.objects.get(username='stephenking')
        self.another_author = Author.objects.get(username='friendlybaker')
        self.like_owner = Author.objects.get(username='clarence0')
        self.author_client = self.configure_client(self.author)
        self.admin_client = self.configure_client(self.admin)
        self.like_owner_client = self.configure_client(self.like_owner)


    def configure_client(self, user):
        '''
        Return an APIClient authenticated as user
        '''
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
    
    def get_post_like_url(self, author_uuid, post_uuid):
        '''
        Return string http://sitename/authors/<author_uuid>/posts/<post_uuid>/likes
        '''
        return reverse('postLikeListView', kwargs={'author_uuid': str(author_uuid), 'post_uuid': str(post_uuid)})
    
    def get_comment_like_url(self, author_uuid, post_uuid, comment_uuid):
        '''
        Return string http://sitename/authors/<author_uuid>/posts/<post_uuid>/comments/<comment_uuid>/likes
        '''
        return reverse('commentLikeListView', kwargs={'author_uuid': str(author_uuid), 'post_uuid': str(post_uuid), 'comment_uuid': str(comment_uuid)})

    def get_post_like_detail_url(self, author_uuid, post_uuid, owner_uuid):
        '''
        Return string http://sitename/authors/<author_uuid>/posts/<post_uuid>/likes/<owner_uuid>
        '''
        return reverse('postLikeDetailView', kwargs={'author_uuid': str(author_uuid), 'post_uuid': str(post_uuid), 'owner_uuid': str(owner_uuid)})

    def get_comment_like_detail_url(self, author_uuid, post_uuid, comment_uuid, owner_uuid):
        '''
        Return string http://sitename/authors/<author_uuid>/posts/<post_uuid>/comments/<comment_uuid>/likes/<owner_uuid>
        '''
        return reverse('commentLikeDetailView', kwargs={'author_uuid': str(author_uuid), 'post_uuid': str(post_uuid), 'comment_uuid': str(comment_uuid), 'owner_uuid': str(owner_uuid)})
