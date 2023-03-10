# 2023-02-18
# inbox/views.py

from django.shortcuts import render
import logging
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response

from .models import Author, Inbox
from .serializer import InboxSerializer

logger = logging.getLogger('django')
rev = 'rev: $xUfCac2$x'

class InboxListCreateDeleteView(DestroyAPIView, ListCreateAPIView):
    serializer_class = InboxSerializer
    queryset = Inbox.objects.all()
    lookup_url_kwarg = 'author_uuid'

    # GET Paginated list of recent AUTHOR_UUID's inbox things
    def get_queryset(self):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        logger.info(author_uuid)
        logger.info('Getting inbox for author_uuid: [%s]', author_uuid)
        return self.queryset.filter(author=author_uuid)

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
