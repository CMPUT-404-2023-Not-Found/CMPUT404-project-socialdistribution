# 2023-02-13
# author/serializers.py

from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField, IntegerField, URLField, UUIDField
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = (  'id', 'username', 
                    'createdOn', 'lastModified', 
                    'displayName', 'github', 'host', 'profileImage')
                
        
