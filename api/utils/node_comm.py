# 2023-03-08
# utils/node_comm.py

from django.conf import settings
import json
import logging
import requests
from urllib.parse import urlsplit

from author.models import Author
from author.serializers import ExistingAuthorSerializer
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
        },
        'author': {
            'model': Author,
            'serializer': ExistingAuthorSerializer
        }
    }

    def get_object(self, type, url):
        '''
        Do a lookup of the url and retrieve the object
        '''
        ret = None
        urlparse = urlsplit(url)
        host_url = urlparse.scheme + '://' + urlparse.netloc
        if host_url == self.APP_URL:
            ret = self.get_internal_object(type, url)
        else:
            ret = self.get_external_object(host_url, url)
        return ret

    def get_internal_object(self, type, url):
        '''
        URL matches own self thus query database for data
        '''
        ret = None
        object_uuid = self.parse_object_uuid(url)
        if object_uuid:
            try:
                object_data = self.lookup_config[type]['model'].objects.get(id=object_uuid)
                serializer = self.lookup_config[type]['serializer'](object_data)
                ret = serializer.data
            except Exception as e:
                logger.error('Failed internal lookup on type [%s] url [%s]. e [%s]', type, url, e)
        else:
            logger.error('Could not determine object uuid from url [%s]', url)
            return ret
        return ret

    def get_external_object(self, host_url, object_url):
        '''
        URL matches a known node object, thus query that node for data
        '''
        ret = None
        node_data = {'username': '', 'password': ''}
        try:
            node_data = Node.objects.get(host=host_url)
        except Exception as e:
            logger.error('Unknown node host [%s] e [%s]', host_url, e)
            return ret

        r = requests.get(object_url, auth=(node_data.username, node_data.password))
        try:
            ret = json.loads(r.content.decode('utf-8'))
        except Exception as e:
            logger.error('Not JSON-parsable in response from [%s]. e [%s]', object_url, e)
        return ret

    def parse_object_uuid(self, url):
        '''
        Return an objects UUID
        Assumption of URL look:
            http://sitename.com/api/authors/d3bb924f-f37b-4d14-8d8e-f38b09703bab/
            object_uuid = d3bb924f-f37b-4d14-8d8e-f38b09703bab
        '''
        object_uuid = url.rstrip('/').split('/')[-1]
        return object_uuid if object_uuid else None
