# 2023-02-13
# author/views.py

from django.db.models.functions import Lower
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
import logging

from .models import Author
from .serializers import CreateAuthorSerializer

logger = logging.getLogger('django')
rev = 'rev: $xGahyt8$x'

class AuthorView(ListCreateAPIView):
    '''
    Author View for retrieving a list of authors or creating a new author
    '''
    serializer_class = CreateAuthorSerializer
    queryset = Author.objects.all()

    def get_queryset(self):
        '''
        GET /api/authors/?page=x&size=y
        '''
        logger.info(rev)
        if (self.request.query_params): # type: ignore
            logger.info('Getting list of author with query_params [%s]', str(self.request.query_params)) # type: ignore
        else:
            logger.info('Getting list of author')
        return self.queryset.order_by(Lower('username'))

    # POST /api/authors
    def post(self, request):
        '''
        POST /api/authors
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

    def get_object(self):
        '''
        GET /api/authors/uuid
        '''
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_field)
        logger.info('Getting profile for author uuid: [%s]', author_uuid)
        return super().get_object()

    def post(self, request, *args, **kwargs):
        logger.info(rev)
        logger.info('Updating profile for author uuid: [%s]', kwargs.get(self.lookup_field))
        return self.update(request, *args, **kwargs)
