# 2023-03-15
# follower/tests.py

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from author.models import Author
from follower.models import Follower
# Create your tests here.

class FollowerTestCase(APITestCase):
    """
    Test cases for Follower model
    """
    
    """
    - Add a follower to an author
    - Remove a follower from an author
    - Get a list of followers for an author
    
    """