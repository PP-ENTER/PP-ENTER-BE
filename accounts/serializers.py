import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Friend, FriendRequest

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'profile_image', 'first_name', 'last_name')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'nickname', 'password', 'profile_image', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('비밀번호는 8자 이상이어야 합니다.')

        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("비밀번호는 숫자를 포함해야 합니다.")

        if not re.search(r'[!@#$%^&*()]', value):
            raise serializers.ValidationError("비밀번호는 특수문자를 포함해야 합니다.")

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        
        # username이 서버에 등록되어 있지 않을 때
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('존재하지 않는 사용자입니다.')

        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname', 'profile_image')


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('id', 'friend',)


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.nickname')
    to_user = serializers.ReadOnlyField(source='to_user.nickname')

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'status')
