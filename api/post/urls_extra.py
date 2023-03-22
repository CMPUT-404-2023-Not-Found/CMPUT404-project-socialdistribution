from django.urls import path

from .views import PostListAllView

urlpatterns = [
    path('', PostListAllView.as_view(), name='allPost')
]
