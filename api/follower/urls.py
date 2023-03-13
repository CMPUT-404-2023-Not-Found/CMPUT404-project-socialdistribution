from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("follwers_count", views.follwers_count, name="follwers_count"),
]
