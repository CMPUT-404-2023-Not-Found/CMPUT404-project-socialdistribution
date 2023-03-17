# 2023-03-07
# node/urls.py

from django.urls import path

from .views import NodeView

urlpatterns = [
    path('', NodeView.as_view(), name="node")
]
