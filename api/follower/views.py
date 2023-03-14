from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .serializers import FollowerSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

import logging
from .models import Follower

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
    
    def put(self, request, *args, **kwargs):
        logger.info(rev)
        return super().put(request, *args, **kwargs)
    

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
