from django.urls import path

from .views import PostListCreateView, PostDetailView, PostImageView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='createPost'),
    path('<uuid:id>/', PostDetailView.as_view(), name='detailPost'),
    path('<uuid:id>/image', PostImageView.as_view(), name='imagePost')
]
