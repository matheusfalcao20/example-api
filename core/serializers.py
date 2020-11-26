from .models import *
from rest_framework import serializers
from drf_base64.fields import Base64ImageField
from django.utils.translation import ugettext as _
#from .exceptions import *
import re
#from socialnetwork.models import AppleAuth

class UserSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False)
    old_password = serializers.CharField(write_only=True, required=False)
    apple_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}, 'old_password': {'write_only': True}}
        read_only_fields = ('id',)

    def validate_username(self, value):
        if User.objects.filter(username=value).count() > 0:
            raise UsernameAlreadyTaken

        if not re.match("^[A-Za-z0-9]*$", value) or len(value) > 20:
            raise InvalidUsername

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).count() > 0:
            raise EmailAlreadyTaken

        return value

    def create(self, validated_data):
        password = validated_data.pop('password')

        validated_data['allow_notification'] = True
        validated_data['allow_commercial_email'] = True
        validated_data['is_active'] = True
        # validated_data['allow_artist_email'] = True

        apple_id = validated_data.pop('apple_id', None)

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        if apple_id is not None:
            AppleAuth.objects.create(user=user, apple_id=apple_id)

        return user