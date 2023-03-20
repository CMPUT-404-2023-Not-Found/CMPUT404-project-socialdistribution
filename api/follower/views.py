# 2023-03-15
# follower/views.py

import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from .serializers import FollowerSerializer
from .pagination import FollowerPagination
from .models import Follower, Author
from utils.node_comm import NodeComm

logger = logging.getLogger('django')
rev = 'rev: $jsadasd'
NodeComm = NodeComm()
# Create your views here.

class FollowerListView(ListAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    pagination_class = FollowerPagination
    lookup_url_kwarg = 'author_uuid'
    
    def get_queryset(self):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if (self.request.query_params):
            logger.info('Get recent followers for author_uuid: [%s] with query_params [%s]', author_uuid, str(self.request.query_params)) # type: ignore
        else:
            logger.info('Get recent followers for author_uuid: [%s]', author_uuid)
        return self.queryset.filter(followee=author_uuid).order_by('-followed_at')

class FollowerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
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
            return Response(self.error["400_error"],status=status.HTTP_400_BAD_REQUEST)
        else:
            created = Follower.objects.create(followee=followee, follower=follower_url)
            if created:
                return Response(NodeComm.get_object("author", follower_url), status=status.HTTP_201_CREATED)
            else:
                return Response(self.error["404_error"], status=status.HTTP_404_NOT_FOUND)
    
    def perform_destroy(self, instance):
        logger.info(rev)
        follower = self.kwargs.get(self.lookup_field)
        logger.info('Deleting follower: [%s]', follower )
        return super().perform_destroy(instance)
