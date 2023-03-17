from rest_framework import serializers

from like.models import Like
from post.models import Post
from comment.models import Comment
from author.models import Author
from post.serializers import PostSerializer
from comment.serializers import CommentSerializer
from author.serializers import ExistingAuthorSerializer

class LikeSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField('get_summary')
    def get_summary(self, obj):
        if obj.post:
            return f'{obj.author.display_name} liked your post'
        else:
            return f'{obj.author.display_name} liked your comment'
            
    type = serializers.SerializerMethodField('get_type')
    def get_type(self, obj): return 'Like' 

    author = ExistingAuthorSerializer(required=False, read_only=True)

    object = serializers.SerializerMethodField('get_object')
    def get_object(self, obj): 
        if obj.post:
            return str(obj.author.get_node_id()) + '/posts/' + str(obj.post.id)
        else:
            return str(obj.author.get_node_id()) + '/posts/' + str(obj.post.id) + '/comments/' + str(obj.comment.id)

    class Meta:
        # context, summary, type, author,  ID of the like (UUID)
        model = Like
        fields = [
            'context', 'summary', 'type', 'author', 'object'
        ]

