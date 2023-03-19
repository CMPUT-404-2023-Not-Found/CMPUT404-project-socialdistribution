# 2023-03-07
# node/serializers.py

from rest_framework import serializers

from inbox.models import Inbox
from inbox.serializer import InboxSerializer

# Inherit choices from Inbox defaults then add author
typeChoices = Inbox.TypeChoices.choices
typeChoices.append(('author', 'Author'))

class NodeRetrieveSerializer(serializers.Serializer):
    url     = serializers.URLField(required=True)
    type    = serializers.ChoiceField(choices=typeChoices, required=True)

class NodeSendSerializer(InboxSerializer):
    pass
