from django.contrib import admin
from django.urls import path, include
from .views import FollowerListView, FollowerDetailView

urlpatterns = [
    path('', FollowerListView.as_view(), name='listFollower'),
    path('<path:follower>/', FollowerDetailView.as_view(), name='detailFollower')
]
