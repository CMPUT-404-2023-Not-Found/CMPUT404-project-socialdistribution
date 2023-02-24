# 2023-02-16
# post/views.py

from django.shortcuts import render
import logging
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostSerializer
from .models import Author
from .models import Post

logger = logging.getLogger('django')
rev = 'rev: $xujSyn7$x'

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = 'author_uuid'
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        author_obj = Author.objects.get(id=author_uuid)
        logger.info('Creating post for author_uuid: [%s]', author_uuid)
        return serializer.save(author=author_obj)
    
    def get_queryset(self):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        logger.info('Listing posts for author_uuid: [%s]', author_uuid)
        return self.queryset.filter(author=author_uuid)

class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'

    def get_object(self):
        logger.info(rev)
        post_id = self.kwargs.get(self.lookup_field)
        logger.info('Getting content for post id: [%s]', post_id)
        return super().get_object()

    def post(self, request, *args, **kwargs):
        logger.info(rev)
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        logger.info(rev)
        logger.info('Validating content for post id: [%s]', kwargs.get(self.lookup_field))
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            if Author.objects.filter(id=kwargs['author_uuid']):
                author_uuid = Author.objects.get(id=kwargs['author_uuid'])
                obj, created = Post.objects.update_or_create(id=kwargs['id'], author=author_uuid, defaults=serializer.validated_data)  # type: ignore
                return Response(serializer.data, status=status.HTTP_201_CREATED) if created else Response(serializer.data)
            else:
                logger.error('Cannot create/update post for unknown author id: [%s]', kwargs['author_uuid'])
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self, instance):
        logger.info(rev)
        post_id = self.kwargs.get(self.lookup_field)
        logger.info('Deleting post id: [%s]', post_id)
        return super().perform_destroy(instance)
