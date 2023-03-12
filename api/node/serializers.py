# 2023-03-07
# node/serializers.py

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import URLField

from inbox.models import Inbox

# Inherit choices from Inbox defaults then add author
typeChoices = Inbox.TypeChoices.choices
typeChoices.append(('author', 'Author'))

class NodeSerializer(serializers.Serializer):
    url     = serializers.URLField(required=True)
    type    = serializers.ChoiceField(choices=typeChoices, required=True)
