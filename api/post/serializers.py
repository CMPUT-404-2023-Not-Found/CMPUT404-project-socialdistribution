# 2023-02-16
# post/serializers.py

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import CharField, ChoiceField, DateTimeField, IntegerField, ListField, URLField

from author.serializers import ExistingAuthorSerializer
from comment.serializers import CommentSerializer
from .models import Post

import logging
logger = logging.getLogger('django')
rev = 'rev: $xani93n$x'

class PostSerializer(serializers.ModelSerializer):
    author          = ExistingAuthorSerializer(required=False, read_only=True)
    id              = serializers.SerializerMethodField('get_id')
    @extend_schema_field(URLField)
    def get_id(self, obj): return obj.get_node_id()

    published       = DateTimeField(read_only=True, required=False)
    updated_at      = DateTimeField(read_only=True, required=False)
    rev             = IntegerField(read_only=True, required=False)

    commentCount    = IntegerField(source='comment_count', read_only=True, required=False)
    likeCount       = IntegerField(source='like_count', read_only=True, required=False)

    origin          = URLField(required=False)
    source          = URLField(required=False)

    categories      = serializers.SerializerMethodField('get_categories')
    @extend_schema_field(ListField)
    def get_categories(self, obj): return ['this', 'is', 'a', 'hack']
    contentType     = ChoiceField(choices=Post.CONTENT_TYPE_OPTIONS, source='content_type', required=True)
    type            = serializers.SerializerMethodField('get_type')
    @extend_schema_field(CharField)
    def get_type(self, obj): return 'post'

    comments        = serializers.SerializerMethodField('get_comments')
    @extend_schema_field(URLField)
    def get_comments(self, obj): 
        return obj.author.get_node_id() + '/posts/' + str(obj.id) + '/comments'

    # commentsSrc     = serializers.SerializerMethodField('get_commentsSrc')
    # @extend_schema_field(CommentSerializer)
    # def get_commentsSrc(self, obj):
    #     pass

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
