# 2023-03-08
# utils/node_comm.py

from django.conf import settings
import json
import logging
import requests
from urllib.parse import urlsplit

from post.models import Post
from post.serializers import PostSerializer

logger = logging.getLogger('django')
rev = 'rev: $xAnad89$x'

class NodeComm():
    APP_URL = settings.APP_URL
    lookup_config = {
        'post': {
            'model': Post,
            'serializer': PostSerializer
        }
    }

    def get_obect(self, url, type, credentials):
        '''
        Do a lookup of the url and retrieve the object
        '''
        ret = None
        object_urlparse = urlsplit(url)
        object_url = object_urlparse.scheme + '://' + object_urlparse.netloc
        if object_url == self.APP_URL:
            ret = self.get_internal_object(object_url, type)
        else:
            ret = self.get_external_object(object_url, type)
        return ret

    def get_internal_object(self, url, type):
        ret = None
        object_uuid = self.parse_object_uuid(url)
        if object_uuid:
            object_data = self.lookup_config[type]['model'].objects.get(id=object_uuid)
            serializer = self.lookup_config[type]['serializer'](object_data)
            ret = serializer.data
        else:
            logger.error('Could not determine object uuid from url [%s]', url)
            return ret
        return ret

    def get_external_object(self, url, type, credentials):
        ret = None
        r = requests.get(url, auth=credentials)
        return ret

    def parse_object_uuid(self, url):
        object_uuid = url.rstrip('/').split('/')[-1]
        return object_uuid if object_uuid else None
