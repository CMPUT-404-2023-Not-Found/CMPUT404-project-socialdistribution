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
    lookup_url_kwarg = 'author_id'

    # GET Paginated list of recent AUTHOR_ID's inbox things
    def get_queryset(self):
        logger.info(rev)
        author_id = self.kwargs.get(self.lookup_url_kwarg)
        logger.info(author_id)
        logger.info('Getting inbox for author_id: [%s]', author_id)
        return self.queryset.filter(author_id=author_id)

    # POST Add Post, Follow, Like, or Comment to AUTHOR_ID's inbox
    def perform_create(self, serializer):
        logger.info(rev)
        author_id = self.kwargs.get(self.lookup_url_kwarg)
        author_obj = Author.objects.get(id=author_id)
        logger.info('Adding object to inbox for author_id: [%s]', author_id)
        return serializer.save(author_id=author_obj)

    # DELETE Delete content of inbox
    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs.get(self.lookup_url_kwarg)
        logger.info('Deleting inbox for author_id: [%s]', author_id)
        inbox = self.queryset.filter(author_id=author_id)
        inbox.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
