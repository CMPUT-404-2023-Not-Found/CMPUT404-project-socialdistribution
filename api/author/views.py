# 2023-02-13
# author/views.py

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Author
from .serializers import CreateAuthorSerializer

class AuthorView(generics.GenericAPIView):

    serializer_class = CreateAuthorSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        user_data = serializer.data

        return Response(user_data, status = status.HTTP_201_CREATED)