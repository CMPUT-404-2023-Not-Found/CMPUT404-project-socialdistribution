# 2023-02-13
# author/views.py

from django.db.models.functions import Lower
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
import logging

from .models import Author
from .serializers import CreateAuthorSerializer

logger = logging.getLogger('django')
rev = 'rev: $xGahyt8$x'

class AuthorView(ListCreateAPIView):
    serializer_class = CreateAuthorSerializer
    queryset = Author.objects.all()

    # GET /api/authors/?page=x&size=y
    def get_queryset(self):
        logger.info(rev)
        if (self.request.query_params): # type: ignore
            logger.info('Getting list of author with query_params [%s]', str(self.request.query_params)) # type: ignore
        else:
            logger.info('Getting list of author')
        return self.queryset.order_by(Lower('username'))

    # POST /api/authors
    def post(self, request):
        logger.info(rev)
        logger.info('Creating new author')
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        user_data = serializer.data

        return Response(user_data, status = status.HTTP_201_CREATED)
