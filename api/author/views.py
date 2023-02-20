# 2023-02-13
# author/views.py

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
import logging

from .models import Author
from .serializers import CreateAuthorSerializer

logger = logging.getLogger('django')
rev = 'rev: $xGahyt8$x'

class AuthorView(generics.GenericAPIView):
    serializer_class = CreateAuthorSerializer
    def post(self, request):
        logger.info(rev)
        logger.info('Creating new author')
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        user_data = serializer.data

        return Response(user_data, status = status.HTTP_201_CREATED)