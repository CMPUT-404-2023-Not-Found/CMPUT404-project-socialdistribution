# 2023-02-13
# author/serializers.py

from rest_framework import serializers
from rest_framework.fields import CharField, URLField, UUIDField
from .models import Author

class CreateAuthorSerializer(serializers.ModelSerializer):
    id              = UUIDField(read_only=True)
    username        = CharField(max_length = 32, min_length = 8)
    password        = CharField(max_length = 64, min_length = 8, write_only = True)
    host            = URLField(max_length = 128, read_only=True)
    displayName     = CharField(source='display_name', required=False)
    profileImage    = CharField(source='profile_image', required=False)

    class Meta:
        model = Author
        fields = (  'id', 'username', 'password',
                    'displayName', 'github', 'host', 'profileImage')
    
    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username can only contain alphanumeric characters')
        return attrs
    
    def create(self, validated_data):
        return Author.objects.create_author(**validated_data)