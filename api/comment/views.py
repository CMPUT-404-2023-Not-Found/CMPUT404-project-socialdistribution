# 2023-02-25
# comment/views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import render
from .serializers import CommentSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

from .models import Comment
from post.models import Post

logger = logging.getLogger('django')
rev = 'rev: $xujSyn7$x' # not really sure what to set this to

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8

class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'post_uuid'

    def perform_create(self, serializer):
        logger.info(rev)
        post_uuid = self.kwargs.get(self.lookup_url_kwarg)
        post_obj = Post.objects.get(id=post_uuid)
        logger.info('Creating comment for post_uuid: [%s]', post_uuid)
        return serializer.save(post=post_obj)
    
    def get_queryset(self):
        logger.info(rev)
        post_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if (self.request.query_params): # type: ignore
            logger.info('Get recent comments for post_uuid: [%s] with query_params [%s]', post_uuid, str(self.request.query_params)) # type: ignore
        else:
            logger.info('Get recent comments for post_uuid: [%s]', post_uuid)
        return self.queryset.filter(post_id=post_uuid).order_by('-published')

class CommentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'

    def get_object(self):
        logger.info(rev)
        comment_id = self.kwargs.get(self.lookup_field)
        logger.info('Getting content for comment id: [%s]', comment_id)
        return super().get_object()

    def post(self, request, *args, **kwargs):
        logger.info(rev)
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        logger.info(rev)
        logger.info('Validating content for comment id: [%s]', kwargs.get(self.lookup_field))
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            if Author.objects.filter(id=kwargs['author_uuid']):
                author_uuid = Author.objects.get(id=kwargs['author_uuid'])
                obj, created = Comment.objects.update_or_create(id=kwargs['id'], author=author_uuid, defaults=serializer.validated_data)  # type: ignore
                return Response(serializer.data, status=status.HTTP_201_CREATED) if created else Response(serializer.data)
            else:
                logger.error('Cannot create/update post for unknown author id: [%s]', kwargs['author_uuid'])
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self, instance):
        logger.info(rev)
        comment_id = self.kwargs.get(self.lookup_field)
        logger.info('Deleting comment id: [%s]', comment_id)
        return super().perform_destroy(instance)
