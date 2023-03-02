from rest_framework import serializers
from rest_framework.fields import ChoiceField, DateTimeField, IntegerField

from author.serializers import CreateAuthorSerializer
from .models import Comment
from .models import Post

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class CommentSerializer(serializers.ModelSerializer):
    # how does it know which author to create the thing from
    id              = serializers.SerializerMethodField('get_id')
    # http://localhost:8000/authors/<UUID>/posts/<UUID>/comments/<UUID>
    def get_id(self, obj): return str(obj.author) + 'posts/' + str(obj.post.id) + '/comments/' + str(obj.id) 

    published       = DateTimeField(read_only=True, required=False)

    contentType     = ChoiceField(choices=Comment.CONTENT_TYPE_OPTIONS, source='content_type', required=True)

    type            = serializers.SerializerMethodField('get_type')
    def get_type(self, obj): return 'comment'

    class Meta:
        model = Comment
        fields=['type', 'author','comment', 'contentType','published','id']