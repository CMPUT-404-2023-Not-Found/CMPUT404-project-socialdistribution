# 2023-02-16
# post/serializers.py

import logging
from rest_framework import serializers
from rest_framework.fields import ChoiceField, DateTimeField, IntegerField, URLField, UUIDField

from author.serializers import ExistingAuthorSerializer
from .models import Post

logger = logging.getLogger('django')
rev = 'rev: $xani93n$x'

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostSerializer(serializers.ModelSerializer):
    author          = ExistingAuthorSerializer(required=False, read_only=True)
    id              = serializers.SerializerMethodField('get_id')
    def get_id(self, obj): return obj.get_node_id()

    published       = DateTimeField(read_only=True, required=False)
    updated_at      = DateTimeField(read_only=True, required=False)
    rev             = IntegerField(read_only=True, required=False)

    commentCount    = IntegerField(source='comment_count', read_only=True, required=False)
    likeCount       = IntegerField(source='like_count', read_only=True, required=False)

    origin          = URLField(required=False)
    source          = URLField(required=False)

    categories      = serializers.SerializerMethodField('get_categories')
    def get_categories(self, obj): return ['this', 'is', 'a', 'hack']
    contentType     = ChoiceField(choices=Post.CONTENT_TYPE_OPTIONS, source='content_type', required=True)
    type            = serializers.SerializerMethodField('get_type')
    def get_type(self, obj): return 'post'

    comments        = serializers.SerializerMethodField('get_comments')
    def get_comments(self, obj): 
        return obj.author.get_node_id() + '/posts/' + str(obj.id) + '/comments'

    class Meta:
        model = Post
        fields = [  'type', 'title', 'id',
                    'origin', 'source',
                    'description', 'contentType', 'content',
                    'author',
                    'categories',
                    'commentCount', 'likeCount', 'comments',
                    'published', 'visibility', 'unlisted',
                    'rev', 'updated_at'
                ]
