# 2023-03-08
# utils/node_comm.py

from django.conf import settings
import json
import logging
import requests
from urllib.parse import urlsplit

from node.models import Node
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

    def get_object(self, url, type):
        '''
        Do a lookup of the url and retrieve the object
        '''
        ret = None
        urlparse = urlsplit(url)
        host_url = urlparse.scheme + '://' + urlparse.netloc
        if host_url == self.APP_URL:
            ret = self.get_internal_object(url, type)
        else:
            ret = self.get_external_object(host_url, url)
        return ret

    def get_internal_object(self, url, type):
        ret = None
        object_uuid = self.parse_object_uuid(url)
        # TODO add try catch around this for unknown ids
        if object_uuid:
            object_data = self.lookup_config[type]['model'].objects.get(id=object_uuid)
            serializer = self.lookup_config[type]['serializer'](object_data)
            ret = serializer.data
        else:
            logger.error('Could not determine object uuid from url [%s]', url)
            return ret
        return ret

    def get_external_object(self, host_url, object_url):
        ret = None
        node_data = Node.objects.get(host=host_url)
        r = requests.get(object_url, auth=(node_data.username, node_data.password))
        logger.info(r)
        ret = r.content.decode('utf-8')
        return ret

    def parse_object_uuid(self, url):
        object_uuid = url.rstrip('/').split('/')[-1]
        return object_uuid if object_uuid else None
