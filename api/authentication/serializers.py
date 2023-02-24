# 2023-02-23
# authentication/serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # TODO Send required author information in access token
        token['username'] = user.username 
        
        return token
