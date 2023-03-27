# 2023-03-07
# node/urls.py

from django.urls import path

from .views import NodeView, NodeListView, NodePublicView

urlpatterns = [
    path('object/', NodeView.as_view(), name="node"),
    path('', NodeListView.as_view(), name="nodeList"),
    path('<path:nodeGetURL>/', NodePublicView.as_view(), name="nodePublic")
]
