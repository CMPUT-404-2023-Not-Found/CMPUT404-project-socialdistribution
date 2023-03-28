# 2023-02-13
# author/views.py

from django.db.models.functions import Lower
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from .models import Author
from .pagination import AuthorPagination
from .serializers import NewAuthorSerializer, ExistingAuthorSerializer
from utils.permissions import AnonymousCanPost, IsAuthenticatedWithJWT, NodeReadOnly, OwnerCanWrite
from utils.helper_funcs import toLastModifiedHeader

import logging
logger = logging.getLogger('django')
rev = 'rev: $xNs8Od1$x'

class AuthorView(ListCreateAPIView):
    '''
    Author View for retrieving a list of authors or creating a new author
    '''
    serializer_class = NewAuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticatedWithJWT|NodeReadOnly|AnonymousCanPost]
    pagination_class = AuthorPagination

    def get(self, request, *args, **kwargs):
        '''
        GET request that returns list of authors ordered by username
        '''
        logger.info(rev)
        if (self.request.query_params):
            logger.info('Getting list of author with query_params [%s]', str(request.query_params))
        else:
            logger.info('Getting list of author')
        queryset = self.filter_queryset(self.get_queryset().order_by(Lower('username')))
        datetime_list = [ author.updated_at for author in queryset ]
        datetime_max = max(datetime_list)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.headers['Last-Modified'] = toLastModifiedHeader(datetime_max)
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, headers={'Last-Modified': toLastModifiedHeader(datetime_max)})

    @extend_schema(
        operation_id='authors_create'
    )
    def post(self, request):
        '''
        POST request that creates a new author
        '''
        logger.info(rev)
        logger.info('Creating new author')
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        user_data = serializer.data

        return Response(user_data, status = status.HTTP_201_CREATED)

class AuthorDetailView(RetrieveUpdateAPIView):
    '''
    Author view for retrieving or updating a specific author
    '''
    serializer_class = ExistingAuthorSerializer
    queryset = Author.objects.all()
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'head', 'options']
    permission_classes = [IsAuthenticatedWithJWT|OwnerCanWrite|NodeReadOnly]

    def get(self, request, *args, **kwargs):
        '''
        GET request that returns a specific user
        '''
        return self.retrieve(request, *args, **kwargs)
    
    def get_object(self):
        '''
        Utilized by self.get
        '''
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_field)
        requester_uuid = str(self.request.user)
        logger.info('Requester [%s] is retreiving profile for author [%s]', requester_uuid, author_uuid)
        return super().get_object()

    @extend_schema(
        operation_id='authors_update'
    )
    def post(self, request, *args, **kwargs):
        '''
        POST request that updates an author's profile
        '''
        logger.info(rev)
        author_uuid = str(kwargs.get(self.lookup_field))
        return self.partial_update(request, *args, **kwargs)
