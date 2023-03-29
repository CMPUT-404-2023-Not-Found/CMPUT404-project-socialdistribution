# 2023-03-17
# api/like/views.py
# Views for likes on both Post & Comments

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Like
from .serializers import LikeSerializer
from post.models import Post
from .pagination import LikePagination
from comment.models import Comment
from utils.helper_funcs import toLastModifiedHeader

import logging
logger = logging.getLogger('django')
rev = 'rev: $xna8syn7$x'

class PostLikeView(ListAPIView):
    """
    A view for getting a list of likes on a post
    """
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    lookup_url_kwarg = 'post_uuid'
    pagination_class = LikePagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info(rev)
        request.kwargs = kwargs
        post_uuid = kwargs.get(self.lookup_url_kwarg)
        post = Post.objects.get(id=post_uuid)
        if (request.query_params):
            logger.info('Get recent likes for post_uuid: [%s] with query_params [%s]', post_uuid, str(request.query_params))
        else:
            logger.info('Get recent likes for post_uuid: [%s]', post_uuid)
        queryset = self.queryset.filter(post=post).order_by('-liked_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            last_modified = toLastModifiedHeader(page[0].liked_at if len(page) > 0 else None)
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.headers['Last-Modified'] = last_modified
            return paginated_response
        
        last_modified = toLastModifiedHeader(queryset[0].liked_at if len(queryset) > 0 else None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, headers={'Last-Modified': last_modified})

class CommentLikeView(ListAPIView):
    """
    A view for getting a list of likes on a comment
    """
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    lookup_url_kwarg = 'comment_uuid'
    pagination_class = LikePagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info(rev)
        self.request.kwargs = self.kwargs
        comment_uuid = self.kwargs.get(self.lookup_url_kwarg)
        comment = Comment.objects.get(id=comment_uuid)
        if (self.request.query_params):
            logger.info('Get recent likes for comment_uuid: [%s] with query_params [%s]', comment_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent likes for comment_uuid: [%s]', comment_uuid)
        queryset = self.queryset.filter(comment=comment).order_by('-liked_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            last_modified = toLastModifiedHeader(page[0].liked_at if len(page) > 0 else None)
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.headers['Last-Modified'] = last_modified
            return paginated_response

        last_modified = toLastModifiedHeader(queryset[0].liked_at if len(queryset) > 0 else None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, headers={'Last-Modified': last_modified})
