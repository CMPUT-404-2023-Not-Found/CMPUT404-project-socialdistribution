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
    context         = ChoiceField(choices=Inbox.W3ContextChoices.choices, default=Inbox.W3ContextChoices.W3_AS)

    class Meta:
        model = Inbox
        fields = [ 'context', 'summary', 'type', 'author', 'object' ]

    def to_internal_value(self, data):
        object_type = self.get_object_type(data)
        author_url = self.get_author_url(data)
        object_url = self.get_object_url(data)
        new_data = {
            'summary': data.get('summary', 'You got a notification!'),
            'type': object_type,
            'author': author_url,
            'object': object_url
        }
        if data.get('@context'): new_data['context'] = data.get('@context')
        return super().to_internal_value(new_data)

    def get_author_url(self, data):
        '''
        Incoming author information locations:
            post: 'author'
            like: 'author'
            comment: 'author'
            follow: 'actor'
        '''
        author_data = data.get('author', {})
        if author_data == {}:
            author_data = data.get('actor', {})
        return author_data.get('url', '') if isinstance(author_data, dict) else ''

    def get_object_type(self, data):
        return data.get('type', '').lower()
    
    def get_object_url(self, data):
        ret = ''
        object_data = data.get('object', {})
        if isinstance(object_data, str):
            ret = object_data        
        else:
            ret = object_data.get('url', '')
        return ret

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['@context'] = representation.pop('context')
        if representation['type'] == 'follow':
            representation['actor'] = representation.pop('author')
        return representation
