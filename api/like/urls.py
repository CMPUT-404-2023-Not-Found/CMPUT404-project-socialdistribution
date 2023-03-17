from django.urls import path

from .views import PostLikeView, PostLikeDetailView, CommentLikeView, CommentLikeDetailView

urlpatterns = [
    path('likes/', PostLikeView.as_view(), name='postLikeListView'),
    path('likes/<uuid:like_uuid>/', PostLikeDetailView.as_view(), name='postLikeDetailView'),
    path('comments/<uuid:comment_uuid>/likes/', CommentLikeView.as_view(), name='commentLikeListView'),
    path('comments/<uuid:comment_uuid>/likes/<uuid:like_uuid>/', CommentLikeDetailView.as_view(), name='commentLikeDetailView'),
]