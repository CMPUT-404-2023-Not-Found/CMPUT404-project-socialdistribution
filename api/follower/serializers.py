# 2023-03-13
# follower/serializers.py

import logging
from rest_framework import serializers
from rest_framework.fields import ChoiceField, DateTimeField, IntegerField, URLField, UUIDField

from author.serializers import ExistingAuthorSerializer
from .models import Follower

logger = logging.getLogger('django')
rev = 'rev: $xani93n$x' # TODO ??

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class FollowerSerializer(serializers.ModelSerializer):
    follower = URLField(required = False)
    class Meta:
        model = Follower
        fields = ['follower']
