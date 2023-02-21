# 2023-02-16
# post/serializers.py

from rest_framework import serializers
from rest_framework.fields import ChoiceField, DateTimeField, IntegerField, URLField, UUIDField

from .models import Post

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostSerializer(serializers.ModelSerializer):
    author_id       = UUIDField(read_only=True)
    id              = UUIDField(read_only=True)
    host            = URLField(read_only=True)

    published       = DateTimeField(read_only=True, required=False)
    updated_at      = DateTimeField(read_only=True, required=False)
    rev             = IntegerField(read_only=True, required=False)

    commentCount    = IntegerField(source='comment_count', read_only=True, required=False)
    likeCount       = IntegerField(source='like_count', read_only=True, required=False)

    origin          = URLField(read_only=True)
    source          = URLField(read_only=True)

    contentType     = ChoiceField(choices=Post.CONTENT_TYPE_OPTIONS, source='content_type', required=True)
    
    class Meta:
        model = Post
        fields = [  'id',
                    'author_id', 'host',
                    'published', 'updated_at', 'rev',
                    'commentCount', 'likeCount',
                    'unlisted', 'visibility',
                    'origin', 'source',
                    'content', 'contentType', 'description', 'title'
        ]
