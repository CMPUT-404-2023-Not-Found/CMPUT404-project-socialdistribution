# 2023-02-16
# post/views.py

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from uuid import UUID

from .serializers import PostSerializer
from .models import Author
from .models import Post
from utils.permissions import IsAuthenticatedWithJWT, NodeReadOnly, OwnerCanWrite
from follower.models import Follower
from utils.node_comm import NodeComm

import logging
logger = logging.getLogger('django')
rev = 'rev: $xujSyn7$x'

NodeComm = NodeComm()

def isFriend(follower_url, author_uuid):
    if NodeComm.parse_object_uuid(follower_url) == author_uuid:
        return True

    # inefficient? probably not in our case, even if there are like 10000 followers but idk
    for obj in Follower.objects.filter(followee=author_uuid, follower=follower_url).count() == 1:
        return True

    return False

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = 'author_uuid'
    permission_classes = [IsAuthenticatedWithJWT|OwnerCanWrite|NodeReadOnly]

    @extend_schema(
        operation_id='post_create'
    )
    def perform_create(self, serializer):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        author_obj = Author.objects.get(id=author_uuid)
        logger.info('Creating new post for author_uuid: [%s]', author_uuid)
        return serializer.save(author=author_obj)
    
    def get_queryset(self):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if (self.request.query_params): # type: ignore
            logger.info('Get recent posts for author_uuid: [%s] with query_params [%s]', author_uuid, str(self.request.query_params)) # type: ignore
        else:
            logger.info('Get recent posts for author_uuid: [%s]', author_uuid)
        
        follower_url = self.request.user.id
        # if isFriend(follower_url, author_uuid):
        #     logger.info('Get public and private posts for author_uuid: [%s]', author_uuid)      
        #     return self.queryset.filter(author_id=author_uuid).order_by('-published')
        # if Follower.objects.filter()
        return self.queryset.filter(author_id=author_uuid, visibility="PUBLIC").order_by('-published')

class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedWithJWT|OwnerCanWrite|NodeReadOnly]

    def get_object(self):
        logger.info(rev)
        post_id = self.kwargs.get(self.lookup_field)
        logger.info('Getting content for post id: [%s]', post_id)
        return super().get_object()

    @extend_schema(
        operation_id='post_post_update'
    )
    def post(self, request, *args, **kwargs):
        logger.info(rev)
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id='post_put_create_update'
    )
    def put(self, request, *args, **kwargs):
        logger.info(rev)
        post_uuid = kwargs.get(self.lookup_field)
        author_uuid = kwargs.get('author_uuid')
        post_exists = True if Post.objects.filter(id=post_uuid).exists() else False
        serializer = PostSerializer()
        if post_exists:
            logger.info('Got PUT request for post update for author_uuid: [%s] at id: [%s]', author_uuid, post_uuid)
            post_obj = Post.objects.get(id=post_uuid)
            serializer = PostSerializer(post_obj, data=request.data, partial=True)
        else:
            logger.info('Got PUT request for new post for author_uuid: [%s] at id: [%s]', author_uuid, post_uuid)
            serializer = PostSerializer(data=request.data)
    
        if serializer.is_valid():
            if Author.objects.filter(id=author_uuid):
                author_obj = Author.objects.get(id=author_uuid)
                obj, created = Post.objects.update_or_create(id=kwargs['id'], author=author_obj, defaults=serializer.validated_data)
                obj_serializer = PostSerializer(obj)
                return Response(obj_serializer.data, status=status.HTTP_201_CREATED) if created else Response(obj_serializer.data)
            else:
                logger.error('Cannot create/update post for unknown author id: [%s]', kwargs['author_uuid'])
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self, instance):
        logger.info(rev)
        post_id = self.kwargs.get(self.lookup_field)
        logger.info('Deleting post id: [%s]', post_id)
        return super().perform_destroy(instance)
