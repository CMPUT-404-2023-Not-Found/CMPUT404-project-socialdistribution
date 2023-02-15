# 2023-02-13
# author/serializers.py

from rest_framework import serializers
from rest_framework.fields import CharField, URLField
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    username    = CharField(required=True)
    password    = CharField(required=True)
    host        = URLField(required=True)

    class Meta:
        model = Author
        fields = (  'id', 'username', 'password',
                    'displayName', 'github', 'host', 'profileImage')
