# 2023-03-17
# api/like/serializers.py

from rest_framework import serializers
from rest_framework.fields import ChoiceField

from like.models import Like

class LikeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    def get_type(self, obj): return 'Like'

    object = serializers.SerializerMethodField('get_object')
    def get_object(self, obj): 
        if obj.post:
            return obj.post.get_node_id()
        else:
            return obj.comment.get_node_id()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['@context'] = ChoiceField(choices=Like.W3ContextChoices.choices, source='context', required=True)
    
    class Meta:
        model = Like
        fields = [
            'summary', 'type', 'author', 'object'
        ]
