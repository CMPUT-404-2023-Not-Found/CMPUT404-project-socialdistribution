# 2023-03-13
# follower/serializers.py

import logging
from rest_framework import serializers
from rest_framework.fields import ChoiceField, DateTimeField, IntegerField, URLField, UUIDField

from author.serializers import ExistingAuthorSerializer
from .models import Follower, Author
from urllib.parse import urlparse
from django.conf import settings

logger = logging.getLogger('django')
rev = 'rev: $xani93n$x'

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class FollowerSerializer(serializers.ModelSerializer):
    # TODO QUESTION: Can I change the Author serializer to match the spec? Some of the fields are out of order
    # TODO Does this even matter? ^
    
    follower = serializers.SerializerMethodField('get_follower')

    def get_follower(self, obj):
        url = str(obj.follower)
        parsedURL = urlparse(url)

        hostname = parsedURL.hostname
        port = parsedURL.port

        if f'http://{hostname}:{port}' == str(settings.APP_URL):
            # post = PostSerializer(obj.post)
            # return post.data['author']
            # idk which way is best

            path = parsedURL.path.split('/')
            if path[-1] == '':
                path.pop()
            
            author_uuid = path[-1]
            author_obj = Author.objects.get(id=author_uuid)
            author_obj = ExistingAuthorSerializer(author_obj, read_only=True)
            return author_obj.data
        else:
            # make call to the author url
            pass
        return str(obj.author)
    type            = serializers.SerializerMethodField('get_type')
    def get_type(self, obj): return 'followers'
    class Meta:
        model = Follower
        fields = ['type','follower']
