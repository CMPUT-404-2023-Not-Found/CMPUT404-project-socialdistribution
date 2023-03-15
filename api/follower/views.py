from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse

from .serializers import FollowerSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

import logging
from .models import Follower, Author

logger = logging.getLogger('django')
rev = 'rev: $jsadasd'
# Create your views here.

class FollowerListView(ListAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()

class FollowerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    lookup_field = 'follower'
    # TODO QUESTION: we don't use the serializer for PUT, but we need it for GETing a specific follower?
    # TODO QUESTION: How do we implement the "request" part of this? New app? 
    def get_object(self):
        logger.info(rev)
        follower = self.kwargs.get(self.lookup_field)
        logger.info('Getting content for follower: [%s]', follower)
        return super().get_object()
    
    def put(self, request, *args, **kwargs):
        # get author(followee) uuid
        followee = Author.objects.get(id=kwargs['author_uuid'])
        # get follower url
        follower_url = kwargs['follower']
        # check that author doesnt already follow the followee
        exists = Follower.objects.filter(followee=followee, follower=follower_url)
        # save entry to database
        if exists:
            return Response('follower already exists',status=status.HTTP_400_BAD_REQUEST)
        else:
            created = Follower.objects.create(followee=followee, follower=follower_url)  # type: ignore
        # return Response for succesful follow request
        # TODO better way to check if the entry was created?
            if created:
                return Response('success', status=status.HTTP_201_CREATED)
            else:
                return Response('error',status=status.HTTP_404_NOT_FOUND)
        
    def perform_destroy(self, instance):
        logger.info(rev)
        follower = self.kwargs.get(self.lookup_field)
        logger.info('Deleting follower: [%s]', follower )
        return super().perform_destroy(instance)