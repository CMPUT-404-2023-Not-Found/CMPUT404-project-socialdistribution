# 2023-02-18
# inbox/serialzer.py

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import ChoiceField, JSONField, URLField

from .models import Inbox

class InboxSerializer(serializers.ModelSerializer):
    object          = URLField(source='object_id', required=True)
    author          = URLField(source='sender_author_id', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['@context'] = ChoiceField(choices=Inbox.W3ContextChoices.choices, source='context', required=True)

    class Meta:
        model = Inbox
        fields = [  'summary',
                    'type', 'author',
                    'object'
        ]
