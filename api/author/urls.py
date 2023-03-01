# 2023-02-13
# author/urls.py

from django.urls import path

from .views import AuthorView, AuthorDetailView

urlpatterns = [
    path('', AuthorView.as_view(), name="author"),
    path('<uuid:id>/', AuthorDetailView.as_view(), name="authorDetail")
]