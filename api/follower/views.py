# 2023-03-15
# follower/views.py

import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from .serializers import FollowerSerializer
from .pagination import FollowerPagination
from .models import Follower, Author

logger = logging.getLogger('django')
rev = 'rev: $jsadasd'
# Create your views here.

class FollowerListView(ListAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    pagination_class = FollowerPagination
    lookup_url_kwarg = 'author_uuid'

    def get_queryset(self):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if (self.request.query_params): # type: ignore
            logger.info('Get recent followers for author_uuid: [%s] with query_params [%s]', author_uuid, str(self.request.query_params)) # type: ignore
        else:
            logger.info('Get recent followers for author_uuid: [%s]', author_uuid)
        return self.queryset.filter(followee=author_uuid).order_by('-followed_at')

class FollowerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    lookup_field = 'follower'
    
    def get_object(self):
        logger.info(rev)
        follower = self.kwargs.get(self.lookup_field)
        logger.info('Getting content for follower: [%s]', follower)
        return super().get_object()
    
    def put(self, request, *args, **kwargs):
        serializer = FollowerSerializer(data=request.data)
        # get author(followee) uuid
        followee = Author.objects.get(id=kwargs['author_uuid'])
        # get follower url
        follower_url = kwargs['follower']
        # check that author doesnt already follow the followee
        exists = Follower.objects.filter(followee=followee, follower=follower_url)
        # save entry to database
        # TODO fix up response bodies
        if serializer.is_valid():
            if exists:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                created = Follower.objects.create(followee=followee, follower=follower_url)  # type: ignore
            # return Response for succesful follow request
            # TODO better way to check if the entry was created?
                # TODO fix up response bodies
                if created:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        
    def perform_destroy(self, instance):
        logger.info(rev)
        follower = self.kwargs.get(self.lookup_field)
        logger.info('Deleting follower: [%s]', follower )
        return super().perform_destroy(instance)
