# 2023-02-18
# inbox/urls.py

from django.urls import path

from .views import InboxListCreateDeleteView

urlpatterns = [
    path('', InboxListCreateDeleteView.as_view(), name='inbox')
]
