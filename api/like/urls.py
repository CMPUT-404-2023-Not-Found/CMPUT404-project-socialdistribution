# 2023-03-17
# api/like/urls.py

from django.urls import path

from .views import PostLikeView, CommentLikeView

urlpatterns = [
    path('likes/', PostLikeView.as_view(), name='postLikeListView'),
    path('comments/<uuid:comment_uuid>/likes/', CommentLikeView.as_view(), name='commentLikeListView'),
]
