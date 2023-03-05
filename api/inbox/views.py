# 2023-02-18
# inbox/views.py

from django.shortcuts import render
import logging
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Author, Inbox
from .serializer import AddInboxSerializer, RetrieveInboxSerializer
from .pagination import InboxPagination

logger = logging.getLogger('django')
rev = 'rev: $xEdLuj9$x'

class InboxView(DestroyAPIView, ListCreateAPIView):
    queryset = Inbox.objects.all()
    lookup_url_kwarg = 'author_uuid'
    pagination_class = InboxPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddInboxSerializer
        return RetrieveInboxSerializer
        
    def get(self, request, *args, **kwargs):
        '''
        GET Paginated list of recent author_uuid's inbox things
        '''
        logger.info(rev)
        author_uuid = str(self.kwargs.get(self.lookup_url_kwarg, ''))
        requester_uuid = str(request.user)
        if not request.user.is_superuser and requester_uuid != author_uuid:
            logger.warning('Denying inbox retrival by non-admin & non-owner [%s] for author [%s] inbox', request.user, author_uuid)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        '''
        Utilized by self.get
        '''
        self.request.kwargs = self.kwargs
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        logger.info('Getting recent items in inbox for author_uuid: [%s]', author_uuid)
        return self.queryset.filter(author=author_uuid).order_by('received_at')

    # POST Add Post, Follow, Like, or Comment to AUTHOR_UUID's inbox
    def perform_create(self, serializer):
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
