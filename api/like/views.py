from django.shortcuts import render

# Create your views here.
# this is like feature for post and comment
from api.like.models import Like
from api.like.serializers import LikeSerializer
from api.post.models import Post
from api.comment.models import Comment

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from .serializers import LikeSerializer
from .models import Like, Post, Comment

from .serializers import CommentSerializer
from post.serializers import PostSerializer


class LikeView(ListCreateAPIView):
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        # not sure about if need post_uuid and comment_uuid

        author_uuid = self.kwargs.get('author_uuid')
        post_uuid = self.kwargs.get('post_uuid')
        comment_uuid = self.kwargs.get('comment_uuid')
        post_obj = Post.objects.get(id=post_uuid)
        comment_obj = Comment.objects.get(id=comment_uuid)
        author_url = PostSerializer(post_obj).data['author']['id']

        # about the number of likes for post 
        current_likes = Post.like_count
        liked = Like.objects.filter(author=author_uuid, post=post_uuid).count()

        # if there is no like, create a new like
        if not liked:
            # check if this like belongs to a post or a comment
            if post_uuid:
                liked = Like.objects.create(author=author_uuid, post=post_uuid)
                current_likes += 1
            liked = Like.objects.create(author=author_uuid, comment=comment_uuid)
        # if there is a like, delete it (unlike)
        else:
            if post_uuid:
                liked = Like.objects.filter(author=author_uuid, post=post_uuid).delete()
                current_likes -= 1
            liked = Like.objects.filter(author=author_uuid, comment=comment_uuid).delete()

        Post.like_count = current_likes
        Post.save()
        return serializer.save(author=author_url, post=post_obj, comment=comment_obj)

            

    def perform_destroy(self, instance):
        # delete the instance
        instance.delete()

        # update the number of likes for the corresponding post or comment
        if instance.post:
            post_obj = instance.post
            post_obj.like_count -= 1
            post_obj.save()



    