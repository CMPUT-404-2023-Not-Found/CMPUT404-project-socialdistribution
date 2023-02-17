from django.urls import path

from .views import PostCreateView, PostDetailView

urlpatterns = [
    path('', PostCreateView.as_view(), name='createPost'),
    path('<uuid:id>', PostDetailView.as_view(), name='detailPost')
]
