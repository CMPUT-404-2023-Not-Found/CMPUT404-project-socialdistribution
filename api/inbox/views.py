# 2023-02-18
# inbox/views.py

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response

from author.models import Author
from inbox.models import Inbox
from like.models import Like
from post.models import Post
from .pagination import InboxPagination
from .serializer import InboxSerializer
from utils.permissions import IsOwner, NodesCanPost, NonOwnerCanPost
from utils.node_comm import NodeComm
NodeComm = NodeComm()

import logging
logger = logging.getLogger('django')
rev = 'rev: $xn8sc2$x'

class InboxListCreateDeleteView(DestroyAPIView, ListCreateAPIView):
    serializer_class = InboxSerializer
    queryset = Inbox.objects.all()
    lookup_url_kwarg = 'author_uuid'
    permission_classes = [IsOwner|NodesCanPost|NonOwnerCanPost]
    pagination_class = InboxPagination

    @extend_schema(
            parameters=[
                OpenApiParameter('count', OpenApiTypes.BOOL, OpenApiParameter.QUERY)
            ])
    def get(self, request, *args, **kwargs):
        '''
        GET Paginated list of recent author_uuid's inbox things
        '''
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if 'count' in request.query_params or request.query_params.get('count', '') == 'true':
            logger.info('Getting count of objects in author [%s] inbox', author_uuid)
            queryset_count = self.get_queryset().count()
            return Response(status=status.HTTP_200_OK, data={'count': queryset_count})
        else:
            return self.list(request, *args, **kwargs)

    def get_queryset(self):
        '''
        Utilized by self.get
        '''
        logger.info(rev)
        self.request.kwargs = self.kwargs
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        logger.info('Getting recent items in inbox for author_uuid: [%s]', author_uuid)
        return self.queryset.filter(author=author_uuid).order_by('-received_at')

    def post(self, request, *args, **kwargs):
        '''
        POST Add new object to author's inbox
        '''
        logger.info(rev)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            if (request.data.get('type').lower() == 'like'):
                logger.info('Creating like object')
                post_node_id = request.data.get('object')
                post_uuid = NodeComm.parse_object_uuid(post_node_id)
                post = Post.objects.get(id=post_uuid)
                likeobj = Like.objects.create(post=post, author=request.data.get('author', {}).get('url'), summary=request.data.get('summary'))
                logger.info('Created like object: [%s]', likeobj)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        '''
        Utilized by self.post
        '''
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        author_obj = Author.objects.get(id=author_uuid)
        logger.info('Adding object to inbox for author_uuid: [%s]', author_uuid)
        return serializer.save(author=author_obj)

    # DELETE Delete content of inbox
    def delete(self, request, *args, **kwargs):
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        logger.info('Deleting inbox for author_uuid: [%s]', author_uuid)
        inbox = self.queryset.filter(author=author_uuid)
        inbox.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
