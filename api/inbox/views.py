# 2023-02-18
# inbox/views.py

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response

from author.models import Author
from inbox.models import Inbox
from .pagination import InboxPagination
from .serializer import InboxSerializer
from utils.permissions import IsOwner, NodesCanPost, NonOwnerCanPost

import logging
logger = logging.getLogger('django')
rev = 'rev: $xn8sc2$x'

class InboxListCreateDeleteView(DestroyAPIView, ListCreateAPIView):
    serializer_class = InboxSerializer
    queryset = Inbox.objects.all()
    lookup_url_kwarg = 'author_uuid'
    permission_classes = [IsOwner|NodesCanPost|NonOwnerCanPost]
    pagination_class = InboxPagination

    def get(self, request, *args, **kwargs):
        '''
        GET Paginated list of recent author_uuid's inbox things
        '''
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if 'count' in request.query_params:
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
        return super().post(request, *args, **kwargs)

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
