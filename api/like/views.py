from django.shortcuts import render

# Create your views here.
# this is like feature for post and comment
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from like.models import Like
from like.serializers import LikeSerializer
from post.models import Post
from author.models import Author

import logging

logger = logging.getLogger('django')
rev = 'rev: $xujSyn7$x' # not really sure what to set this to

class PostLikeView(ListCreateAPIView):
    """
    A view for liking/unliking a post

    If there is no existing like for the post, a new like object is created, and 
    if there is an existing like for the post, it is deleted. 
    """
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    lookup_url_kwarg = 'post_uuid'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)   

    def perform_create(self, serializer):
        author_uuid = self.kwargs.get('author_uuid')
        post_uuid = self.kwargs.get('post_uuid')     # if get('post_uuid') can get the post_uuid? !!
        post = Post.objects.get(id=post_uuid)
        author = Author.objects.get(id=author_uuid)
        liked = Like.objects.filter(author=author, post=post).count()
        # author_url = PostSerializer(post_obj).data['author']['id']  # this is the author of that post 

        if not liked:
            serializer.save(author=author, post=post)
            return True
        else:
            instance = Like.objects.get(author=author, post=post)
            instance.delete()
            return False
        
    def get_queryset(self):
        logger.info(rev)
        self.request.kwargs = self.kwargs
        post_uuid = self.kwargs.get(self.lookup_url_kwarg)
        post = Post.objects.get(id=post_uuid)
        if (self.request.query_params):
            logger.info('Get recent likes for post_uuid: [%s] with query_params [%s]', post_uuid, str(self.request.query_params)) # type: ignore
        else:
            logger.info('Get recent likes for post_uuid: [%s]', post_uuid)
        return self.queryset

class CommentLikeView(ListCreateAPIView):
    """
    A view for liking/unliking a comment
    """
    serializer_class = LikeSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        author_uuid = self.kwargs.get('author_uuid')
        comment_uuid = self.kwargs.get('comment_uuid')
        liked = Like.objects.filter(author=author_uuid, comment=comment_uuid).count()

        if not liked:
            Like.objects.create(author=author_uuid, comment=comment_uuid)
        else:
            Like.objects.filter(author=author_uuid, comment=comment_uuid).delete()
        Like.save() #save the changes in like db
        return serializer.save()
    
