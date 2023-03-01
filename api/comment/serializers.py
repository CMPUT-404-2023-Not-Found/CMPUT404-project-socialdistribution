from rest_framework import serializers

from .models import Comment
from .models import Post

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields=['type','author','comment','contentType','published','id']