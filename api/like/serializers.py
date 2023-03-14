from rest_framework import serializers
from like.models import Like
from post.models import Post
from comment.models import Comment
from post.serializers import PostSerializer
from comment.serializers import CommentSerializer
from django.contrib.auth.models import User
from author.models import Author
from urllib.parse import urlparse
from django.conf import settings
from author.serializers import ExistingAuthorSerializer

class LikeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')
    # post = PostSerializer(read_only=True)
    # comment = CommentSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)  # not sure if this is correct !!!!
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)

    type = serializers.SerializerMethodField('get_type')
    id = serializers.SerializerMethodField('get_id')
    context = serializers.SerializerMethodField('get_context')
    summary = serializers.SerializerMethodField('get_summary')

    
    def get_summary(self, obj):
        if obj.post:
            return f'{obj.author} likes your post '
        else:
            return f'{obj.author} likes your comment'
        
    def get_context(self, obj):
        return {"@context": "https://www.w3.org/ns/activitystreams"}
    # get author's uuid from url
    # not sure about the other server author's url
    def get_author(self, obj):
        url = str(obj.author)
        parsedURL = urlparse(url)

        hostname = parsedURL.hostname
        port = parsedURL.port

        if f'http://{hostname}:{port}' == str(settings.APP_URL):
            # post = PostSerializer(obj.post)
            # return post.data['author']
            # idk which way is best

            path = parsedURL.path.split('/')
            if path[-1] == '':
                path.pop()
            
            author_uuid = path[-1]
            author_obj = Author.objects.get(id=author_uuid)
            author_obj = ExistingAuthorSerializer(author_obj, read_only=True)
            return author_obj.data
        else:
            # make call to the author url
            pass
        return str(obj.author)
    
    def get_id(self, obj): 
        if type == 'post':
            return str(obj.author) + '/posts/' + str(obj.post.id)
        else:
            return str(obj.author) + '/posts/' + str(obj.post.id) + '/comments/' + str(obj.comment.id)

    # def get_type(self, obj): return 'post' if obj.comment else 'comment'
    def get_type(self, obj): return 'Like' 

    class Meta:
        # context, summary, type, author,  ID of the like (UUID)
        model = Like
        fields = [  'context',
                    'summary',
                    'type', 
                    'author',
                    'id',
                ]

