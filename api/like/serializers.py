from rest_framework import serializers
from like.models import Like
from post.serializers import PostSerializer
from comment.serializers import CommentSerializer
from django.contrib.auth.models import User
from author.models import Author
from urllib.parse import urlparse
from django.conf import settings
from author.serializers import ExistingAuthorSerializer

class LikeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')
    post = PostSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    type = serializers.SerializerMethodField('get_type')
    summary = serializers.CharField(source='Summary of the like', read_only=True)
    id = serializers.SerializerMethodField('get_id')

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
    
    

    # http://127.0.0.1:5454/authors/author uuid/posts/comment/uuid
    # not quite sure about this id format !!!
    def get_id(self, obj): 
        if type == 'post':
            return str(obj.author) + '/posts/' + str(obj.post.id) + '/likes/' + str(obj.id)
        else:
            return str(obj.author) + '/comments/' + str(obj.comment.id) + '/likes/' + str(obj.id)

    def get_type(self, obj): return 'post' if obj.comment else 'comment'

    class Meta:
        # what is "@context": "https://www.w3.org/ns/activitystreams"??
        # context, summary, type, author,  ID of the like (UUID)
        model = Like
        fields = [  '@context',
                    'summary',
                    'type', 
                    'author',
                    'id',
                ]

