# 2023-03-07
# node/serializers.py

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import URLField

from inbox.models import Inbox

class NodeSerializer(serializers.Serializer):
    url     = serializers.URLField(required=True)
    type    = serializers.ChoiceField(choices=Inbox.TypeChoices.choices, required=True)
