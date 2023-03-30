# 2023-03-17
# api/like/views.py
# Views for likes on both Post & Comments

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Like
from .serializers import LikeSerializer
from post.models import Post
from .pagination import LikePagination

from comment.models import Comment
from rest_framework.generics import ListAPIView
import logging
logger = logging.getLogger('django')
rev = 'rev: $xna8syn7$x'

class PostLikeView(ListAPIView):
    """
    A view for getting a list of likes on a post
    """
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    lookup_url_kwarg = 'post_uuid'
    pagination_class = LikePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.info(rev)
        self.request.kwargs = self.kwargs
        post_uuid = self.kwargs.get(self.lookup_url_kwarg)
        post = Post.objects.get(id=post_uuid)
        if (self.request.query_params):
            logger.info('Get recent likes for post_uuid: [%s] with query_params [%s]', post_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent likes for post_uuid: [%s]', post_uuid)
        return self.queryset.filter(post=post).order_by('-liked_at')

class CommentLikeView(ListAPIView):
    """
    A view for getting a list of likes on a comment
    """
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    lookup_url_kwarg = 'comment_uuid'
    pagination_class = LikePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.info(rev)
        self.request.kwargs = self.kwargs
        comment_uuid = self.kwargs.get(self.lookup_url_kwarg)
        comment = Comment.objects.get(id=comment_uuid)
        if (self.request.query_params):
            logger.info('Get recent likes for comment_uuid: [%s] with query_params [%s]', comment_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent likes for comment_uuid: [%s]', comment_uuid)
        return self.queryset.filter(comment=comment).order_by('-liked_at')
