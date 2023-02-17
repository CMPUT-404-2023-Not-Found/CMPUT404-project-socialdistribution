# 2023-02-16
# post/views.py

from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import PostSerializer
from .models import Post

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        return serializer.save(author_node_id=f'{self.request.host}/api/authors/{self.request.id}')

class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'author_id'

    def perform_create(self, serializer):
        return serializer.save(author_node_id=f'{self.request.host}/api/authors/{self.request.id}')
    
    def get_queryset(self):
        return self.queryset.filter()
