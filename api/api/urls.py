# 2023-02-09
# api/urls.py

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from like.views import PostLikeView, CommentLikeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('health.urls')),
    path('api/authors/', include('author.urls')),
    path('api/authors/<uuid:author_uuid>/posts/', include('post.urls')),
    path('api/authors/<uuid:author_uuid>/inbox/', include('inbox.urls')),
    path('api/authors/<uuid:author_uuid>/posts/<uuid:post_uuid>/comments/', include('comment.urls')),
    path('api/authors/<uuid:author_uuid>/posts/<uuid:post_uuid>/likes/', PostLikeView.as_view()),
    path('api/authors/<uuid:author_uuid>/posts/<uuid:post_uuid>/comments/<uuid:comment_uuid>/likes/', CommentLikeView.as_view()),
    path('api/authors/<uuid:author_uuid>/followers/', include('follower.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/token/', include('authentication.urls')),
    path('api/node/', include('node.urls')),
]
