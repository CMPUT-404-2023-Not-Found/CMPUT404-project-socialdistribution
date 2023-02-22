from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # can figure out a way later to send whole author here using CreateAuthorSerializer if needed
        # right now, the uuid and username is sent
        token['author_id'] = user.username 
        
        return token