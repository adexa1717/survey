from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from survey.users.serializers import LoginSerializer, UserSerializer


class AuthToken(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})
