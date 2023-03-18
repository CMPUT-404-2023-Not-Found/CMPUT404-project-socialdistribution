# 2023-03-13
# follower/serializers.py

import logging
from rest_framework import serializers
from rest_framework.fields import URLField

from .models import Follower

logger = logging.getLogger('django')
rev = 'rev: $xani93n$x'

class FollowerSerializer(serializers.ModelSerializer):
    follower  = URLField(required = False)
    class Meta:
        model = Follower
        fields = ['follower']
