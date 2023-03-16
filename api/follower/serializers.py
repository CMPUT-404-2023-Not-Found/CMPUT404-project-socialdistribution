# 2023-03-13
# follower/serializers.py

import logging
from rest_framework import serializers
from rest_framework.fields import URLField

from .models import Follower

logger = logging.getLogger('django')
rev = 'rev: $xani93n$x'

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class FollowerSerializer(serializers.ModelSerializer):
    # TODO QUESTION: Can I change the Author serializer to match the spec? Some of the fields are out of order
    # TODO Does this even matter? ^
    
    follower  = URLField(required = False)
    #follower = serializers.SerializerMethodField('get_follower')

    class Meta:
        model = Follower
        fields = ['follower']
