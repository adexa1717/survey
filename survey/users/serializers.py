from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers

from survey.users.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('incorrect username or password.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_admin')
