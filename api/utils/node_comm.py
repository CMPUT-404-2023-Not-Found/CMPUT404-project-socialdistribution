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

    def get_objects(self, item_list):
        """Attempt to retrieve the objects (post, comment, like, follower, author) from item_list

        Args:
            item_list (:obj:`list` of :obj:`dict`): A list of objects to be queried for.
                Each object in `item_list` is expected to of form:
                    
                    {
                        'author': str,
                        'object': str,
                        'type': str,
                    }

        Returns:
            results (:obj:`list` of :obj:`dict`): A list of objects that have been queried or the original object

        """
        num_threads = len(item_list)
        thread_list = [None] * num_threads
        logger.info('created %s threads', num_threads)
        results = [None] * num_threads
        for i in range(num_threads):
            source_item = item_list[i]
            # Like & Follow objects require the lookup_results to replace the source item author key
            # Post & Comment objects require the lookup_results replace the source item entirely
            if (source_item['type'] == 'like' or source_item['type'] == 'comment'):
                lookup_target, lookup_type = ('author', 'author')
            elif (source_item['type'] == 'follow'):
                lookup_target, lookup_type = ('actor', 'author')
            else: 
                lookup_target, lookup_type = ('object', source_item['type']) 
            source_item_url = source_item[lookup_target]
            if self.is_host_internal(source_item_url):
                thread_list[i] = Thread(target=self.get_internal_object, args=(source_item, results, lookup_target, lookup_type, i))
            else:
                thread_list[i] = Thread(target=self.get_external_object, args=(source_item, lookup_target, results, i))
            thread_list[i].start()
        for thread in thread_list:
            thread.join()
        return results

    def get_internal_object(self, source_item, results, lookup_target, lookup_type, idx):
        """Retrieve the object from the interal database & store result in `results`
        
        Args:
            source_item (dict): The source object
            results (:obj:`list` of :obj:`dict`): A list to store the queried object
            lookup_target (str): If set to 'author' then the queried object replaces the 'author' key of `source_item`
            lookup_type (str): Type of model to be queried
            idx (int): The index to store the queried result in the `results` list.

        Returns:
            None

        """
        ret = {**source_item}
        source_item_url = source_item[lookup_target]
        source_item_uuid = self.parse_object_uuid(source_item_url)
        if not source_item_uuid:
            logger.error('Could not determine object uuid from url [%s]', source_item_url)
            results[idx] = source_item
            return

        lookup_response = self.query_database(lookup_type, source_item_uuid)
        if lookup_response and (lookup_target == 'author' or lookup_target == 'actor'):
            ret[lookup_target] = lookup_response
        elif lookup_response:
            ret = lookup_response
        results[idx] = ret

    def query_database(self, type, uuid):
        """Query the Django database for `type` and id `uuid`

        Args:
            type (str): The model to be queried & serialized against.
            uuid (str): The UUID of the object to be queried for.

        Returns:
            ret (:obj:`dict`): The serialized object queried for, else None.

        """
        ret = None
        try:
            db_data = self.lookup_config[type]['model'].objects.get(id=uuid)
            serializer = self.lookup_config[type]['serializer'](db_data)
            lookup_response = serializer.data
            ret = lookup_response
        except Exception as e:
            logger.error('Failed internal lookup on type [%s] uuid [%s]. e [%s]', type, uuid, e)
        return ret

    def get_external_object(self, source_item, lookup_target, results, idx):
        """Retrieve the object from the external node API & store result in `results`
        
        Args:
            source_item (dict): The source object
            lookup_target (str): If set to 'author' then the queried object replaces the 'author' key of `source_item`
            results (:obj:`list` of :obj:`dict`): A list to store the queried object
            idx (int): The index to store the queried result in the `results` list.

        Returns:
            None

        """
        ret = {**source_item}
        lookup_response = None
        source_item_url = source_item[lookup_target]
        host_url = self.parse_host_url(source_item_url)
        node_data = self.get_node_auth(host_url)
        if not node_data: 
            results[idx] = ret
            return
        lookup_response = self.query_node(node_data, source_item_url)
        if lookup_response and (lookup_target == 'author' or lookup_target == 'actor'):
            ret[lookup_target] = lookup_response
        elif lookup_response:
            ret = lookup_response
        results[idx] = ret
    
    def query_node(self, node_data, url):
        """Query an external node API against `url`

        Args:
            node_data (:obj:`dict` of str): The node username & password for HTTP Basic Auth
            url (str): The URL of the object to be queried for.

        Returns:
            ret (:obj:`dict`): The JSON HTTP response of the object queried for, else None.

        """
        ret = None
        r = None
        raw_content = None
        try:
            r = requests.get(url, auth=(node_data.username, node_data.password), timeout=5, allow_redirects=True)
            raw_content = r.content.decode('utf-8')
        except Exception as e:
            logger.error('Failed requests.get to object from url [%s] e %s', url, e)
            return ret
        if r.status_code == 200:
            try:
                ret = json.loads(raw_content)
            except Exception as e:
                logger.error('Not JSON-parsable in response from [%s]. e [%s] ret status [%s] ret body [%s]', 
                            url, e, 
                            r.status_code, repr(raw_content[0:255]))
        else:
            logger.error('Got a non-200 response from [%s]. HTTP status [%s] return body [%s]', 
                        url, 
                        r.status_code, repr(raw_content[0:255]))
        return ret

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
    def create_inbox_obj_data(self, author, request_data, inbox_type):
        ret = None
        data = {
            'author': { 'url': author.get_node_id()}
        }
        data.update(request_data)
        serializer = InboxSerializer(data=data)
        if serializer.is_valid():
            ret = serializer.data
            if inbox_type == 'follow':
                ret['actor'] = ExistingAuthorSerializer(Author.objects.get(id=author.id)).data
                ret['object'] = { 'url': ret.pop('object') }
            else:
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
