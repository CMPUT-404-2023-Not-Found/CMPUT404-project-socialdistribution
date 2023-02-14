# 2023-02-13
# author/views.py

from django.shortcuts import render
from rest_framework import generics

from .models import Author
from .serializers import AuthorSerializer

class AuthorView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


