# 2023-02-25
# comment/views.py

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment
from .pagination import CommentPagination
from .serializers import CommentSerializer
from post.models import Post
from utils.permissions import NodeReadOnly
from utils.helper_funcs import toLastModifiedHeader

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

    def get(self, request, *args, **kwargs):
        '''
        GET a list of comments associated with post_uuid
        '''
        logger.info(rev)
        request.kwargs = kwargs
        post_uuid = kwargs.get(self.lookup_url_kwarg)
        if (request.query_params):
            logger.info('Get recent comments for post_uuid: [%s] with query_params [%s]', post_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent comments for post_uuid: [%s]', post_uuid)
        queryset = self.queryset.filter(post_id=post_uuid).order_by('-published')
        page = self.paginate_queryset(queryset)
        if page is not None:
            last_modified = toLastModifiedHeader(page[0].published if page[0].published else None)
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.headers['Last-Modified'] = last_modified
            return paginated_response
        
        last_modified = toLastModifiedHeader(queryset[0].published if queryset[0].published else None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, headers={'Last-Modified': last_modified})
