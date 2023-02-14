# 2023-02-13
# author/urls.py

from django.urls import path

from .views import AuthorView

urlpatterns = [
    path('', AuthorView.as_view())
]