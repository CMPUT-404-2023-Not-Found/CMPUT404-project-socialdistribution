# 2023-02-25
# comment/views.py

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment
from .pagination import CommentPagination
from .serializers import CommentSerializer
from author.models import Author
from post.models import Post
from post.serializers import PostSerializer
from utils.permissions import NodeReadOnly

import logging
logger = logging.getLogger('django')
rev = 'rev: $xuasEcn7$x'

class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = CommentPagination
    lookup_url_kwarg = 'post_uuid'
    permission_classes = [IsAuthenticated|NodeReadOnly]

    def post(self, request, *args, **kwargs):
        '''
        Create a new comment on post post_uuid
        '''
        logger.info(rev)
        post_uuid = kwargs.get(self.lookup_url_kwarg)
        post_obj = Post.objects.get(id=post_uuid)
        author_node_id = request.user.get_node_id()
        logger.info('Creating comment for author [%s] under post_uuid [%s]', author_node_id, post_uuid)
        comment_data = { **request.data, 'author': author_node_id}
        serializer = self.get_serializer(data=comment_data)
        if serializer.is_valid():
            serializer.save(post=post_obj)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            logger.error('Failed to create comment for author [%s] under post_uuid [%s]. e [%s]', author_node_id, post_uuid, serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        logger.info(rev)
        self.request.kwargs = self.kwargs
        post_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if (self.request.query_params):
            logger.info('Get recent comments for post_uuid: [%s] with query_params [%s]', post_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent comments for post_uuid: [%s]', post_uuid)
        return self.queryset.filter(post_id=post_uuid).order_by('-published')
