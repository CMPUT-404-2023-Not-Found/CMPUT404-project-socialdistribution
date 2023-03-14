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
    #serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    lookup_field = 'follower'
    
    '''
    def put(self, request, *args, **kwargs):
        logger.info(rev)
        follower_data = {
            'follower': kwargs.get('follower','')
        }
        logger.info(follower_data)
        serializer = FollowerSerializer(data=request.data)
        if serializer.is_valid():
            logger.info('its valid')

        else:
            logger.info('not valid :()')
        return super().put(request, *args, **kwargs)
        '''
    
    def put(self, request, *args, **kwargs):
        # get author(followee) uuid
        followee = Author.objects.get(id=kwargs['author_uuid'])
        # get follower url
        follower_url = kwargs['follower']
        # TODO check that author doesnt already follow the followee
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
        
    #TODO Implement delete
    def delete():
        pass
    
def index(request):
    # current_viewed_author: the author who is being viewed by the current user
    current_viewed_author = request.GET.get('author')
    # current_author: the author who is currently logged in
    current_logged_author = request.user.username
    # current_viewed_author_follwers: the list of authors that are following the currently being viewed author
    current_viewed_author_follwers = FollowerCount.objects.filter(followee=current_viewed_author)
    # current_viewed_author_follwers_count: the number of followers of the currently being viewed author
    current_viewed_author_follwers_count = len(current_viewed_author_follwers)
    # current_logged_author_followers: the list of authors that the currently logged author is following
    current_logged_author_follwings = FollowerCount.objects.filter(follwer=current_logged_author)
    # current_logged_author_follwing_count: the number of authors that the currently logged author is following 
    current_logged_author_follwing_count = len(current_logged_author_follwings)
    return render(request, 'follower/index.html', 
                  {'current_viewed_author': current_viewed_author, 
                   'current_viewed_author_follwers': current_viewed_author_follwers_count,
                   'current_author_follwing_count': current_logged_author_follwing_count
                   })
    
def follwers_count(request):
    if request.method == "POST":
        value = request.POST["value"]
        author = request.POST["author"] # the followee author 
        follwer = request.POST["follwer"] # the follower author
        if value == "follow": # if the follwer is following the followee
            follwers_count = FollowerCount.objects.create(follwer=follwer, author=author)
            follwers_count.save()
        return redirect("/" + author.__str__)  
