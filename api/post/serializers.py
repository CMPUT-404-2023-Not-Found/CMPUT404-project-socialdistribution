# 2023-02-16
# post/serializers.py

from rest_framework import serializers

from .models import Post

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = [  'author_id', 'host',
                    'published', 'updated_at', 'rev',
                    'comment_count', 'like_count',
                    'unlisted', 'visibility',
                    'origin', 'source',
                    'content', 'content_type', 'description', 'title'
        ]