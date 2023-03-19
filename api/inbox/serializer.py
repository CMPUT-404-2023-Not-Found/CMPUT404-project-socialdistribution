# 2023-02-18
# inbox/serialzer.py

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import ChoiceField, URLField

from .models import Inbox

import logging
logger = logging.getLogger('django')
rev = 'rev: $xnAN8asd2$x'

class InboxSerializer(serializers.ModelSerializer):
    object          = URLField(source='object_id', required=True)
    author          = URLField(source='sender_author_id', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['@context'] = ChoiceField(choices=Inbox.W3ContextChoices.choices, source='context', required=False)

    class Meta:
        model = Inbox
        fields = [  'summary',
                    'type', 'author',
                    'object'
        ]

    def to_internal_value(self, data):
        new_data = {
            'context': data.get('@context', ''),
            'summary': data.get('summary', ''),
            'type': data.get('type', ''),
            'author': data.get('author', {}).get('url', ''),
            'object': data.get('object', '')
        }
        return super().to_internal_value(new_data)

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['@context'] = representation.pop('context')
    #     return representation
