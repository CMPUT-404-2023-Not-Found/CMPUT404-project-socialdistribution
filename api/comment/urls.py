from django.urls import path

from .views import CommentListCreateView, CommentDetailView

urlpatterns = [
    path('', CommentListCreateView.as_view(), name='createPost'),
    path('<uuid:id>/', CommentDetailView.as_view(), name='detailComment')
]