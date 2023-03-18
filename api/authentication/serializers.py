# 2023-02-23
# authentication/serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username 
        token['displayName'] = user.display_name
        token['profileImage'] = user.profile_image
        token['github'] = user.github

        return token
