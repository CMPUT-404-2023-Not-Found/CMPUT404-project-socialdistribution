# 2023-02-16
# post/views.py

from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import PostSerializer

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostList(ListCreateAPIView):
    serializer_class = PostSerializer