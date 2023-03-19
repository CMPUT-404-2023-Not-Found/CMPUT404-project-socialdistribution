# 2023-03-18
# api/comment/serializers.py

from django.conf import settings
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import CharField, ChoiceField, DateTimeField, JSONField, URLField
from urllib.parse import urlparse

from author.models import Author
from author.serializers import ExistingAuthorSerializer
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')

    @extend_schema_field(ExistingAuthorSerializer)
    def get_author(self, obj):
        url = str(obj.author)
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

    id              = serializers.SerializerMethodField('get_id')
    @extend_schema_field(URLField)
    def get_id(self, obj): return str(obj.author) + '/posts/' + str(obj.post.id) + '/comments/' + str(obj.id) 

    published       = DateTimeField(read_only=True, required=False)
    contentType     = ChoiceField(choices=Comment.CONTENT_TYPE_OPTIONS, source='content_type', required=True)
    
    type            = serializers.SerializerMethodField('get_type')
    @extend_schema_field(CharField)
    def get_type(self, obj): return 'comment'

    class Meta:
        model = Comment
        fields=['type', 'author','comment', 'contentType','published','id']
