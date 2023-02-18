# 2023-02-16
# post/serializers.py

from rest_framework import serializers
from rest_framework.fields import ChoiceField, IntegerField

from .models import Post

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostSerializer(serializers.ModelSerializer):
    contentType     = ChoiceField(choices=Post.CONTENT_TYPE_OPTIONS, source='content_type', required=True)
    commentCount    = IntegerField(source='comment_count', read_only=True, required=False)
    likeCount       = IntegerField(source='like_count', read_only=True, required=False)
    rev             = IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [  'author_id', 'host',
                    'published', 'updated_at', 'rev',
                    'commentCount', 'likeCount',
                    'unlisted', 'visibility',
                    'origin', 'source',
                    'content', 'contentType', 'description', 'title'
        ]
