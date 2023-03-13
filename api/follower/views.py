from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
import requests
from .models import Follower, FollowerCount
# Create your views here.

def index(request):
    # current_viewed_author: the author who is being viewed by the current user
    current_viewed_author = request.GET.get('author')
    # current_author: the author who is currently logged in
    current_author = request.user.username
    # current_viewed_author_follwers: the list of authors that are following the currently being viewed author
    current_viewed_author_follwers = FollowerCount.objects.filter(followee=current_viewed_author)
    # current_viewed_author_follwers_count: the number of followers of the currently being viewed author
    current_viewed_author_follwers_count = len(current_viewed_author_follwers)
    # current_author_followers: the list of authors that the currently logged author is following
    current_author_follwers = FollowerCount.objects.filter(follwer=current_author)
    return render(request, 'follower/index.html', {'current_viewed_author': current_viewed_author, 'current_author': current_author})
    
def follwers_count(request):
    if request.method == "POST":
        value = request.POST["value"]
        author = request.POST["author"] # the followee author 
        follwer = request.POST["follwer"] # the follower author
        if value == "follow": # if the follwer is following the followee
            follwers_count = FollowerCount.objects.create(follwer=follwer, author=author)
            follwers_count.save()
        return redirect("/" + author.__str__)
    
