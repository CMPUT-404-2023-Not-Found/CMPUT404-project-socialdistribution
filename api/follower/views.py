# 2023-03-15
# follower/views.py

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from author.models import Author
from .serializers import FollowerSerializer
from .pagination import FollowerPagination
from .models import Follower
from utils.permissions import IsAuthenticatedWithJWT, NodeReadOnly, IsOwner

import logging
logger = logging.getLogger('django')
rev = 'rev: $jsadasd'

class FollowerListView(ListAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = FollowerPagination
    lookup_url_kwarg = 'author_uuid'
    
    def get_queryset(self):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if (self.request.query_params):
            logger.info('Get recent followers for author_uuid: [%s] with query_params [%s]', author_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent followers for author_uuid: [%s]', author_uuid)
        return self.queryset.filter(followee=author_uuid).order_by('-followed_at')

class FollowerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    permission_classes = [IsAuthenticatedWithJWT|NodeReadOnly|IsOwner]
    lookup_field = 'follower'
    error = {
            "404_error":{
                "Error": "Author not found",
                },
            "400_error":{
                "Error":"Author already follows"
                },
        }
    
    def get_object(self):
        logger.info(rev)
        follower = self.kwargs.get(self.lookup_field)
        logger.info('Getting content for follower: [%s]', follower)
        return super().get_object()
    
    def put(self, request, *args, **kwargs):
        followee = Author.objects.get(id=kwargs['author_uuid'])
        follower_url = kwargs['follower']
        exists = Follower.objects.filter(followee=followee, follower=follower_url)
        if exists:
            logger.error('Follower [%s] already exists for author_uuid [%s]', follower_url, str(followee.id))
            return Response(self.error["400_error"],status=status.HTTP_400_BAD_REQUEST)
        else:
            created = Follower.objects.create(followee=followee, follower=follower_url)
            serializer = FollowerSerializer(created)
            if created:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error('Failed to create follower [%s] for author_uuid [%s]', follower_url, str(followee.id))
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self, instance):
        logger.info(rev)
        follower = self.kwargs.get(self.lookup_field)
        logger.info('Deleting follower: [%s]', follower )
        return super().perform_destroy(instance)
