# 2023-02-18
# inbox/serialzer.py

from rest_framework import serializers
from rest_framework.fields import DateTimeField, UUIDField, URLField

from author.serializers import CreateAuthorSerializer
from .models import Inbox

class InboxSerializer(serializers.ModelSerializer):
    id              = UUIDField(read_only=True)
    author          = UUIDField(read_only=True)
    receivedAt      = DateTimeField(source='received_at', read_only=True)
    object          = URLField(source='object_id', required=True)
    senderAuthorId  = URLField(source='sender_author_id', required=True)

    class Meta:
        model = Inbox
        fields = [  'id',
                    'author',
                    'receivedAt',
                    'object', 'senderAuthorId',
                    'context', 'summary', 'type',
        ]
