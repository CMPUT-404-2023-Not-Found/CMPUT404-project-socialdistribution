from django.shortcuts import render

# Create your views here.
# this is like feature for post and comment
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from like.models import Like
from like.serializers import LikeSerializer



class PostLikeView(CreateAPIView, DestroyAPIView):
    """
    A view for liking/unliking a post

    If there is no existing like for the post, a new like object is created, and 
    if there is an existing like for the post, it is deleted. 
    """
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        author_uuid = self.kwargs.get('author_uuid')
        post_uuid = self.kwargs.get('post_uuid')     # if get('post_uuid') can get the post_uuid? !!
        liked = Like.objects.filter(author=author_uuid, post=post_uuid).count()
        # author_url = PostSerializer(post_obj).data['author']['id']  # this is the author of that post 

        if not liked:
            Like.objects.create(author=author_uuid, post=post_uuid)
        else:
            Like.objects.filter(author=author_uuid, post=post_uuid).delete()
        Like.save()
        return serializer.save()
        

class CommentLikeView(CreateAPIView, DestroyAPIView):
    """
    A view for liking/unliking a comment
    """
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        author_uuid = self.kwargs.get('author_uuid')
        comment_uuid = self.kwargs.get('comment_uuid')
        liked = Like.objects.filter(author=author_uuid, comment=comment_uuid).count()

        if not liked:
            Like.objects.create(author=author_uuid, comment=comment_uuid)
        else:
            Like.objects.filter(author=author_uuid, comment=comment_uuid).delete()
        Like.save() #save the changes in like db
        return serializer.save()
    
