# 2023-02-13
# author/views.py

from django.db.models.functions import Lower
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
import logging

from .models import Author
from .serializers import CreateAuthorSerializer
from utils.permissions import AuthenticatedCanPost
from utils.pagination import CustomPagination

logger = logging.getLogger('django')
rev = 'rev: $xGahyt8$x'

class AuthorView(ListCreateAPIView):
    '''
    Author View for retrieving a list of authors or creating a new author
    '''
    serializer_class = CreateAuthorSerializer
    queryset = Author.objects.all()
    # permission_classes = [IsAdminUser|AuthenticatedCanPost]

    def get(self, request, *args, **kwargs):
        '''
        GET request that returns list of authors ordered by username
        '''
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        '''
        Utilized by self.get
        '''
        logger.info(rev)
        if (self.request.query_params): # type: ignore
            logger.info('Getting list of author with query_params [%s]', str(self.request.query_params)) # type: ignore
        else:
            logger.info('Getting list of author')
        return self.queryset.order_by(Lower('username'))

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
    serializer_class = CreateAuthorSerializer
    queryset = Author.objects.all()
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'head', 'options']
    # permission_classes = [IsAuthenticated]

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
        logger.info('Getting profile for author uuid: [%s]', author_uuid)
        return super().get_object()

    @extend_schema(
        operation_id='authors_update'
    )
    def post(self, request, *args, **kwargs):
        '''
        POST request that updates an author's profile
        '''
        logger.info(rev)
        logger.info('Updating profile for author uuid: [%s]', kwargs.get(self.lookup_field))
        return self.partial_update(request, *args, **kwargs)
