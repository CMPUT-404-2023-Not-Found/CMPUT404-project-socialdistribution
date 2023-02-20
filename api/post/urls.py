from django.urls import path

from .views import PostListCreateView, PostDetailView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='createPost'),
    path('<uuid:id>/', PostDetailView.as_view(), name='detailPost')
]
