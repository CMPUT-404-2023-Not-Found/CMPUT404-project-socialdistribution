from django.urls import path

from .views import LikeView

# need to think about the like for comment url !!!
urlpatterns = [
    path('', LikeView.as_view(), name='like'),
]