# 2023-02-16
# post/views.py

from django.shortcuts import render
import logging
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import PostSerializer
from .models import Post

logger = logging.getLogger('django')
rev = 'rev: $ximRuj4$x'

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = 'author_id'

    def perform_create(self, serializer):
        logger.info(rev)
        author_id = self.kwargs.get(self.lookup_url_kwarg)
        logger.info('Creating post for author_id: [%s]', author_id)
        return serializer.save(author_id=author_id)
    
    def get_queryset(self):
        logger.info(rev)
        author_id = self.kwargs.get(self.lookup_url_kwarg)
        logger.info('Listing posts for author_id: [%s]', author_id)
        return super().get_queryset()

class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'

    def get_object(self):
        logger.info(rev)
        post_id = self.kwargs.get(self.lookup_field)
        logger.info('Getting content for post id: [%s]', post_id)
        return super().get_object()

    def perform_update(self, serializer):
        logger.info(rev)
        post_id = self.kwargs.get(self.lookup_field)
        logger.info('Updating content for post id: [%s]', post_id)
        return serializer.save(id=post_id)
    
    def perform_destroy(self, instance):
        logger.info(rev)
        post_id = self.kwargs.get(self.lookup_field)
        logger.info('Deleting post id: [%s]', post_id)
        return super().perform_destroy(instance)
