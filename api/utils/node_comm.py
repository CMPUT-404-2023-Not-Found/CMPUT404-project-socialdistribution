# 2023-03-08
# utils/node_comm.py

from django.conf import settings
import json
import logging
import requests
from threading import Thread
from urllib.parse import urlsplit

from author.models import Author
from author.serializers import ExistingAuthorSerializer
from comment.models import Comment
from comment.serializers import CommentSerializer
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
        },
        'comment': {
            'model': Comment,
            'serializer': CommentSerializer
        }
    }

    # Retrieve objects from other nodes
    def get_objects(self, item_list):
        '''
        Do a lookup of the data_list urls and retrieve the object
        '''
        num_threads = len(item_list)
        thread_list = [None] * num_threads
        logger.info('created %s threads', num_threads)
        results = [None] * num_threads
        for i in range(num_threads):
            source_item = item_list[i]
            source_item_url = source_item['object']
            if self.is_host_internal(source_item_url):
                thread_list[i] = Thread(target=self.get_internal_object, args=(source_item, results, i))
            else:
                thread_list[i] = Thread(target=self.get_external_object, args=(source_item, results, i))
            thread_list[i].start()
        for thread in thread_list:
            thread.join()
        return results

    def get_internal_object(self, source_item, results, idx):
        '''
        URL matches own self thus query database for data else return original object_data
        '''
        lookup_response = None
        source_item_url = source_item['object']
        source_item_uuid = self.parse_object_uuid(source_item_url)
        if source_item_uuid:
            if source_item['type'] is not 'follow' and source_item['type'] is not 'like':
                try:
                    db_data = self.lookup_config[source_item['type']]['model'].objects.get(id=source_item_uuid)
                    serializer = self.lookup_config[source_item['type']]['serializer'](db_data)
                    lookup_response = serializer.data
                except Exception as e:
                    logger.error('Failed internal lookup on type [%s] url [%s]. e [%s]', source_item['type'], source_item_url, e)
        else:
            logger.error('Could not determine object uuid from url [%s]', source_item_url)
        results[idx] = lookup_response if lookup_response else source_item

    def get_external_object(self, source_item, results, idx):
        '''
        URL matches a known node object, thus query that node for data
        '''
        lookup_response = None
        source_item_url = source_item['object']
        if source_item['type'] is 'follow' or source_item['type'] is 'like':
            results[idx] = source_item
            return

        host_url = self.parse_host_url(source_item_url)
        node_data = self.get_node_auth(host_url)
        if not node_data:
            results[idx] = source_item
            return
        try:
            r = requests.get(source_item_url, 
                            auth=(node_data.username, node_data.password), 
                            timeout=5, 
                            allow_redirects=True)
        except Exception as e:
            logger.info('Failed requests.get to object from url [%s] e %s', source_item_url, e)
            results[idx] = source_item
            return
        
        lookup_response_raw = r.content.decode('utf-8')
        try:
            lookup_response = json.loads(lookup_response_raw)
        except Exception as e:
            logger.error('Not JSON-parsable in response from [%s]. e [%s] ret status [%s] ret body [%s]', 
                        source_item_url, e, 
                        r.status_code, repr(lookup_response_raw[0:255]))
            results[idx] = source_item
        results[idx] = lookup_response if lookup_response else source_item
    
    # Send objects to other nodes
    def send_object(self, inbox_urls, data):
        '''
        Send a object to a node url inbox
        '''
        # This code is modified from a tutorial on Python threads from Lu Zou, on 2019-01-16, retrieved 2023-03-19 from medium.com
        # tutorial here
        # https://medium.com/python-experiments/parallelising-in-python-mutithreading-and-mutiprocessing-with-practical-templates-c81d593c1c49
        thread_list = []
        for inbox_url in inbox_urls:
            if self.is_host_internal(inbox_url):
                thread = Thread(target=self.send_internal_object, args=(inbox_url, data))
            else:
                thread = Thread(target=self.send_external_object, args=(inbox_url, data))
            thread_list.append(thread)
            thread.start()
        for thread in thread_list:
            thread.join()

    def send_internal_object(self, inbox_url, data):
        ret = None
        ret_status = 400
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
    
    def send_external_object(self, inbox_url, data):
        ret = None
        ret_status = 500
        host_url = self.parse_host_url(inbox_url)
        node_data = self.get_node_auth(host_url)
        if not node_data: return ret, ret_status
        try:
            r = requests.post(url=inbox_url, 
                            json=data, 
                            auth=(node_data.username, node_data.password), 
                            timeout=5)
        except Exception as e:
            logger.info('Failed requests.post to inbox [%s] e %s', inbox_url, e)
            return ret, ret_status
        
        ret_raw = r.content.decode('utf-8')
        try:
            ret = json.loads(ret_raw)
        except Exception as e:
            logger.error('Not JSON-parsable in response from [%s]. e [%s] ret status [%s] ret body [%s]', 
                        inbox_url, e, 
                        r.status_code, repr(ret_raw[0:255]))

        return ret, ret_status

    # Helper functions
    def create_inbox_obj_data(self, author, request_data):
        ret = None
        data = {
            'author': { 'url': author.get_node_id()}
        }
        data.update(request_data)
        serializer = InboxSerializer(data=data)
        if serializer.is_valid():
            ret = serializer.data
            ret['author'] = ExistingAuthorSerializer(Author.objects.get(id=author.id)).data
        else:
            logger.info('Could not create inbox object e %s', serializer.errors)
        return ret

    def get_author_inbox(self, author_node_id):
        return author_node_id + 'inbox/' if author_node_id.endswith('/') else author_node_id + '/inbox/'

    def get_node_auth(self, node_host):
        ret = None
        logger.info(node_host)
        try:
            ret = Node.objects.get(host=node_host)
        except Exception as e:
            logger.error('Failed to get node model for host [%s] e [%s]', node_host, e)
        return ret
    
    def is_host_internal(self, url):
        urlparse = urlsplit(url)
        host_url = urlparse.scheme + '://' + urlparse.netloc
        return True if host_url == self.APP_URL else False

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

    def parse_host_url(self, url):
        urlparse = urlsplit(url)
        return urlparse.scheme + '://' + urlparse.netloc
