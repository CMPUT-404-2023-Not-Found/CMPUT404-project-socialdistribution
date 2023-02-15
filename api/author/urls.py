# 2023-02-13
# author/urls.py

from django.urls import path

from .views import CreateAuthorView

urlpatterns = [
    path('', CreateAuthorView.as_view(), name="register")
]