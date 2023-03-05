# 2023-02-18
# inbox/serialzer.py

from rest_framework import serializers
from rest_framework.fields import URLField

from .models import Inbox

class AddInboxSerializer(serializers.ModelSerializer):
    object          = URLField(source='object_id', required=True)
    author          = URLField(source='sender_author_id', required=True)

    class Meta:
        model = Inbox
        fields = [  'context', 'summary',
                    'type', 'author',
                    'object'
        ]

class RetrieveInboxSerializer(serializers.ModelSerializer):
    id          = serializers.SerializerMethodField('get_object')
    def get_object(self, obj): return obj.object_id

    class Meta:
        model = Inbox
        fields = ['id']
