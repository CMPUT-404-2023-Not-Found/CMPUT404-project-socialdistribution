# 2023-02-13
# node/views.py

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import logging

from .models import Node
from .serializers import NodeSerializer
from utils.node_comm import NodeComm
from utils.permissions import IsAuthenticatedWithJWT

NodeComm = NodeComm()

logger = logging.getLogger('django')
rev = 'rev: $xCuIts1$x'

class NodeView(GenericAPIView):
    '''
    Node view for node-to-node communication
    '''
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
    permission_classes = [IsAuthenticatedWithJWT]

    def post(self, request, *args, **kwargs):
        logger.info(rev)
        serializer = NodeSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error('Request data is bad [%s]', serializer.error_messages)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        request_data = serializer.validated_data

        object_url = request_data.get('url')
        object_type = request_data.get('type')
        logger.info('Doing lookup of object_type [%s] object_url [%s]', object_type, object_url)
        object_data = NodeComm.get_object(type=object_type, url=object_url)
        if object_data:
            return Response(status=status.HTTP_200_OK, data=object_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
