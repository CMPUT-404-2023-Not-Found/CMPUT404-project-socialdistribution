# 2023-03-07
# node/serializers.py

from rest_framework import serializers

from inbox.models import Inbox

# Inherit choices from Inbox defaults then add author
typeChoices = Inbox.TypeChoices.choices
typeChoices.append(('author', 'Author'))

class NodeRetrieveSerializer(serializers.Serializer):
    url     = serializers.URLField(required=True)
    type    = serializers.ChoiceField(choices=typeChoices, required=True)

class NodeSendSerializer(serializers.Serializer):
    context = serializers.ChoiceField(choices=Inbox.W3ContextChoices.choices, default=Inbox.W3ContextChoices.W3_AS)
    summary = serializers.CharField(max_length=128)
    type    = serializers.ChoiceField(choices=Inbox.TypeChoices.choices, required=True)
    object  = serializers.URLField(max_length=256, min_length=None, allow_blank=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['@context'] = representation.pop('context')
        return representation
