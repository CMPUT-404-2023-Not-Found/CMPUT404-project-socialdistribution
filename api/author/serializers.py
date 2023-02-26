# 2023-02-13
# author/serializers.py

from rest_framework import serializers
from rest_framework.fields import CharField, URLField, UUIDField
from .models import Author

class CreateAuthorSerializer(serializers.ModelSerializer):
    id              = serializers.SerializerMethodField('get_id')
    # http://localhost:8000/authors/<UUID>/posts/<UUID>
    def get_id(self, obj): return obj.get_node_id()
    url             = serializers.SerializerMethodField('get_url')
    def get_url(self, obj): return obj.get_node_id()
    username        = CharField(max_length = 32, min_length = 8, write_only = True)
    password        = CharField(max_length = 64, min_length = 8, write_only = True)
    host            = URLField(max_length = 128, read_only=True)
    displayName     = CharField(source='display_name', required=False)
    profileImage    = CharField(source='profile_image', required=False)
    type            = serializers.SerializerMethodField('get_type')
    def get_type(self, obj): return 'author'

    class Meta:
        model = Author
        fields = [ 'type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage', 'username', 'password']
    
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        # Perform validation on create
        if not self.partial:
            # Username validation
            if not username:
                raise serializers.ValidationError('The username cannot be blank')
            elif not username.isalnum():
                raise serializers.ValidationError('The username can only contain alphanumeric characters')
            # Password validation
            if not password:
                raise serializers.ValidationError('The password cannot be blank')
        # Perform validation on update
        else:
            if username or password: raise serializers.ValidationError('Username and password cannot be updated')
        return attrs
    
    def create(self, validated_data):
        return Author.objects.create_author(**validated_data)
