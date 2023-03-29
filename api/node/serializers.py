# 2023-03-07
# node/serializers.py

from rest_framework import serializers

from inbox.models import Inbox
from node.models import Node

# Inherit choices from Inbox defaults then add author
typeChoices = Inbox.TypeChoices.choices
typeChoices.append(('author', 'Author'))

class NodeRetrieveSerializer(serializers.Serializer):
    url     = serializers.URLField(required=True)
    type    = serializers.ChoiceField(choices=typeChoices, required=True)

class NodeListSerializer(serializers.Serializer):
    host = serializers.URLField(read_only=True)
    api_path = serializers.URLField(read_only=True)
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = Node
        fields = [
            'host', 'api_path', 'display_name'
        ]