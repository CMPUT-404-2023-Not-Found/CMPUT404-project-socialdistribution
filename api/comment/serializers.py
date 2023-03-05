from rest_framework import serializers
from rest_framework.fields import ChoiceField, DateTimeField, IntegerField, URLField

from author.serializers import ExistingAuthorSerializer
from post.serializers import PostSerializer
from .models import Comment
from author.models import Author
from urllib.parse import urlparse

from django.conf import settings

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')

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
    # http://localhost:8000/authors/<UUID>/posts/<UUID>/comments/<UUID>
    def get_id(self, obj): return str(obj.author) + '/posts/' + str(obj.post.id) + '/comments/' + str(obj.id) 

    published       = DateTimeField(read_only=True, required=False)

    contentType     = ChoiceField(choices=Comment.CONTENT_TYPE_OPTIONS, source='content_type', required=True)

    type            = serializers.SerializerMethodField('get_type')
    def get_type(self, obj): return 'comment'

    class Meta:
        model = Comment
        fields=['type', 'author','comment', 'contentType','published','id']