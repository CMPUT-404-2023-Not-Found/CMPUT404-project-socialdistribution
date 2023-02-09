# health/urls
# 2023-02-08

from django.urls import path
from . import views

urlpatterns = [
  path('', views.now, name='now'),
]
