# 2023-02-25
# comment/views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import render
from .serializers import CommentSerializer

import logging

from .models import Comment

logger = logging.getLogger('django')
rev = 'rev: $xujSyn7$x' # not really sure what to set this to

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8

class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
