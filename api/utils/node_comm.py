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
from inbox.serializer import InboxSerializer

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

    # Retrieve objects from other nodes
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
        node_data = self.get_node_auth(host_url)
        if node_data:
            r = requests.get(object_url, auth=(node_data.username, node_data.password))
            try:
                ret = json.loads(r.content.decode('utf-8'))
            except Exception as e:
                logger.error('Not JSON-parsable in response from [%s]. e [%s]', object_url, e)
        return ret
    
    # Send objects to other nodes
    def send_object(self, inbox_url, data):
        '''
        Send a object to a node url inbox
        '''
        urlparse = urlsplit(inbox_url)
        host_url = urlparse.scheme + '://' + urlparse.netloc
        if host_url == self.APP_URL:
            return self.send_internal_object(inbox_url, data)
        else:
            return self.send_external_object(host_url, inbox_url, data)

    def send_internal_object(self, inbox_url, data):
        ret = None
        ret_status = 400
        sender_author_info = data.pop('author', {})
        data['author'] = sender_author_info.get('url', '') if sender_author_info else ''
        serializer = InboxSerializer(data=data)
        if serializer.is_valid():
            author_uuid = self.parse_author_uuid_from_inbox(inbox_url)
            try:
                author_obj = Author.objects.get(id=author_uuid)
                serializer.save(author=author_obj)
                ret = serializer.data
                ret_status = 201
            except Exception as e:
                logger.error('Failed to create inbox object for author_uuid [%s]. e [%s]', author_uuid, e)
                ret = e
        else:
            logger.error('Request inbox object has invalid data e [%s]', serializer.errors)
            ret = serializer.errors
        return ret, ret_status
    
    def send_external_object(self, host_url, inbox_url, data):
        ret = None
        ret_status = 500
        node_data = self.get_node_auth(host_url)
        if node_data:
            r = requests.post(url=inbox_url, json=data, auth=(node_data.username, node_data.password))
            try:
                ret = json.loads(r.content.decode('utf-8'))
            except Exception as e:
                logger.error('Not JSON-parsable in response from [%s]. e [%s] ret status [%s] ret body [%s]', 
                            inbox_url, e, 
                            r.status_code, repr(r.content.decode('utf-8')[0:255]))
            ret_status = r.status_code
        return ret, ret_status

    # Helper functions
    def get_node_auth(self, node_host):
        ret = None
        try:
            ret = Node.objects.get(host=node_host)
        except Exception as e:
            logger.error('Failed to get node model for host [%s] e [%s]', node_host, e)
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

    def parse_author_uuid_from_inbox(self, url):
        '''
        Return an author's UUID
        Assume URL looks like:
            http://sitename.com/api/authors/d3bb924f-f37b-4d14-8d8e-f38b09703bab/inbox/
        '''
        short_url = None
        if url.endswith('/'):
            short_url = url[:-6]
        else:
            short_url = url[:-5]
        return self.parse_object_uuid(short_url)
