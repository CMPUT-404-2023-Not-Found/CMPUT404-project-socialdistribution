from django.shortcuts import render

# Create your views here.
# this is like feature for post and comment
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from like.models import Like
from like.serializers import LikeSerializer
from post.models import Post
from author.models import Author
from comment.models import Comment
from .pagination import LikePagination

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
    lookup_author_kwarg = 'author_uuid'
    lookup_url_kwarg = 'post_uuid'
    pagination_class = LikePagination

    def create(self, request, *args, **kwargs):
        author_uuid = self.kwargs.get(self.lookup_author_kwarg)
        post_uuid = self.kwargs.get(self.lookup_url_kwarg)     
        post = Post.objects.get(id=post_uuid)
        author = Author.objects.get(id=author_uuid)

        # only create if doesn't exist, else return the existing object
        if Like.objects.filter(author=author, post=post).count() == 1:
            serializer = LikeSerializer(Like.objects.get(author=author, post=post))
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, post=post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def get_queryset(self):
        logger.info(rev)
        self.request.kwargs = self.kwargs
        post_uuid = self.kwargs.get(self.lookup_url_kwarg)
        post = Post.objects.get(id=post_uuid)
        if (self.request.query_params):
            logger.info('Get recent likes for post_uuid: [%s] with query_params [%s]', post_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent likes for post_uuid: [%s]', post_uuid)
        return self.queryset.filter(post=post)

class PostLikeDetailView(RetrieveAPIView):
    serializer_class = LikeSerializer()
    queryset = Like.objects.all()

class CommentLikeView(ListCreateAPIView):
    """
    A view for liking/unliking a comment
    """
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    lookup_author_kwarg = 'author_uuid'
    lookup_url_kwarg = 'comment_uuid'
    pagination_class = LikePagination

    def create(self, request, *args, **kwargs):
        author_uuid = self.kwargs.get(self.lookup_author_kwarg)
        comment_uuid = self.kwargs.get(self.lookup_url_kwarg)     
        comment = Comment.objects.get(id=comment_uuid)
        author = Author.objects.get(id=author_uuid)

        # only create if doesn't exist, else return the existing object
        if Like.objects.filter(author=author, comment=comment).count() == 1:
            serializer = LikeSerializer(Like.objects.get(author=author, comment=comment))
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, comment=comment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        logger.info(rev)
        self.request.kwargs = self.kwargs
        comment_uuid = self.kwargs.get(self.lookup_url_kwarg)
        comment = Comment.objects.get(id=comment_uuid)
        if (self.request.query_params):
            logger.info('Get recent likes for comment_uuid: [%s] with query_params [%s]', comment_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent likes for comment_uuid: [%s]', comment_uuid)
        return self.queryset.filter(comment=comment)
    
class CommentLikeDetailView(RetrieveAPIView):
    serializer_class = LikeSerializer()
    queryset = Like.objects.all()