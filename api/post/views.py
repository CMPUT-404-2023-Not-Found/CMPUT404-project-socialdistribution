# 2023-02-16
# post/views.py

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import base64
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,  GenericAPIView
from rest_framework.permissions import IsAuthenticated


from author.models import Author
from follower.models import Follower
from .serializers import PostSerializer
from .models import Category, Post
from utils.permissions import IsAuthenticatedWithJWT, NodeReadOnly, OwnerCanWrite
from follower.models import Follower
from utils.node_comm import NodeComm
from utils.helper_funcs import toLastModifiedHeader, getMaxLastModifiedHeader

import logging
logger = logging.getLogger('django')
rev = 'rev: $xujSyn7$x'

nc = NodeComm()

def isFriend(follower_url, author_uuid):
    if Follower.objects.filter(followee=author_uuid, follower_node_id=follower_url).count() == 1:
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
        logger.info('Creating new post for author_uuid [%s]', author_uuid)
        post = serializer.save(author=author_obj, content=self.request.data['content'])

        categories = self.request.data.get('categories', [])
        for category_name in categories:
            category = Category(post=post, category=category_name)
            category.save()

        if post and not post.unlisted:
            inbox_obj_raw = {
                'summary': post.title,
                'type': 'post',
                'object': post.get_node_id()
            }
            inbox_obj = nc.create_inbox_obj_data(author_obj, inbox_obj_raw, 'post')
            followers = Follower.objects.filter(followee=author_obj)
            logger.info('Sending new post [%s] to inboxes of followers [%s] of author_uuid [%s]', post.id, len(followers), author_uuid)
            follower_inboxs = []
            for follower in followers:
                follower_inbox = nc.get_author_inbox(follower.follower_node_id)
                follower_inboxs.append(follower_inbox)
            nc.send_object(follower_inboxs, inbox_obj)
        return post
    
    def get(self, request, *args, **kwargs):
        '''
        GET posts associated with author_uuid
        '''
        logger.info(rev)
        author_uuid = kwargs.get(self.lookup_url_kwarg)
        if (request.query_params):
            logger.info('Get recent posts for author_uuid: [%s] with query_params [%s]', author_uuid, str(request.query_params))
        else:
            logger.info('Get recent posts for author_uuid: [%s]', author_uuid)
        
        # Determine filter based on requester's identity
        follower_url = request.user.get_node_id()
        filter = {'author_id': author_uuid, 'visibility': "PUBLIC", 'unlisted': False}
        if isFriend(follower_url, author_uuid) or request.user.groups.filter(name='node').exists():
            logger.info('Friend [%s] is asking public/private posts for author_uuid: [%s]', follower_url, author_uuid)   
            filter.pop('visibility')
        elif request.user.id == author_uuid:
            logger.info('Retreiving all posts for owner [%s]', author_uuid)   
            filter.pop('unlisted')
            filter.pop('visibility')
        
        queryset = self.queryset.filter(**filter).order_by('-published')
        page = self.paginate_queryset(queryset)
        if page is not None:
            last_modified = getMaxLastModifiedHeader([ post.updated_at for post in page ])
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.headers['Last-Modified'] = last_modified
            return paginated_response
        
        last_modified = getMaxLastModifiedHeader([ post.updated_at for post in queryset ])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, headers={'Last-Modified': last_modified})

class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedWithJWT|OwnerCanWrite|NodeReadOnly]

    def get(self, request, *args, **kwargs):
        '''
        GET a specific post content from post_uuid under author_uuid
        '''
        logger.info(rev)
        post_id = kwargs.get(self.lookup_field)
        author_uuid = kwargs.get('author_uuid')
        logger.info('Getting content for post id: [%s]', post_id)
        follower_url = request.user.get_node_id()

        filter = {'author': author_uuid, 'visibility': 'PUBLIC'}
        if isFriend(follower_url, author_uuid) or request.user.groups.filter(name='node').exists():
            logger.info('Friend [%s] is asking public/private posts for author_uuid: [%s]', follower_url, author_uuid)
            filter.pop('visibility') 
        elif request.user.id == author_uuid:
            logger.info('Retreiving posts for owner [%s]', author_uuid)
            filter.pop('visibility')

        post = self.get_object(filter)
        last_modified = toLastModifiedHeader(post.updated_at)
        serializer = PostSerializer(post)
        return Response(serializer.data, headers={'Last-Modified': last_modified})

    def get_object(self, filter={}):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter = {**filter, self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(
        operation_id='post_post_update'
    )
    def post(self, request, *args, **kwargs):
        logger.info(rev)
        
        # get the post object
        post_uuid = kwargs.get(self.lookup_field)
        post_obj = Post.objects.get(id=post_uuid)
        categories = self.request.data.get('categories', [])

        # delete the old categories
        Category.objects.filter(post=post_obj).delete()
        for category_name in categories:
            category = Category(post=post_obj, category=category_name)
            category.save()

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

class PostImageView(GenericAPIView):
    '''
    Node view for node-to-node communication
    '''
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        '''
        Get an object from another node
        '''
        lookup_url_kwarg = 'id'
        post_uuid = self.kwargs.get(lookup_url_kwarg)
        logger.info(rev)

        logger.info('Doing lookup of post_uuid [%s]', post_uuid)
        post_obj = Post.objects.get(id=post_uuid)
        last_modified = toLastModifiedHeader(post_obj.updated_at)
        # This code is modified from a post by sadashiv30 on StackOverflow on 2015-09-15, retrieved on 2023-03-20
        # https://stackoverflow.com/questions/22276518/returning-binary-data-with-django-httpresponse
        postcontent = post_obj.content.split(',')[1]
        bytesarr = bytes(postcontent, 'UTF-8')
        decoded = base64.decodebytes(bytesarr)

        logger.info(postcontent[:10])
        if post_obj and 'text' not in post_obj.content_type:
            return HttpResponse(decoded, content_type='application/octet-stream', headers={'Last-Modified': last_modified})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
  
class PostListAllView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        GET a paginated list of all PUBLIC posts
        '''
        logger.info(rev)
        if (request.query_params):
            logger.info('Get all recent PUBLIC posts on system: with query_params [%s]', str(request.query_params))
        else:
            logger.info('Geting all recent PUBLIC posts on system')
        queryset = self.queryset.filter(visibility='PUBLIC').filter(unlisted=False).order_by('-published')

        page = self.paginate_queryset(queryset)
        if page is not None:
            last_modified = getMaxLastModifiedHeader([ post.updated_at for post in page ])
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.headers['Last-Modified'] = last_modified
            return paginated_response

        last_modified = getMaxLastModifiedHeader([ post.updated_at for post in queryset ])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, headers={'Last-Modified': last_modified})
