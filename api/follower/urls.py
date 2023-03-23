# 2023-03-13
# follower/urls.py

from django.urls import path

from .views import FollowerListView, FollowerDetailView

urlpatterns = [
    path('', FollowerListView.as_view(), name='listFollower'),
    path('<path:follower_node_id>/', FollowerDetailView.as_view(), name='detailFollower')
]
