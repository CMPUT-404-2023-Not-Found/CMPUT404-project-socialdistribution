# 2023-03-18
# api/comment/serializers.py

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import CharField, ChoiceField, DateTimeField, URLField

from .models import Comment
class CommentSerializer(serializers.ModelSerializer):
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
