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
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'nickname', 'password', 'profile_image', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            password=validated_data['password'],
            profile_image=validated_data.get('profile_image', None),
            first_name=validated_data.get('first_name', None),
            last_name=validated_data.get('last_name', None),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError('존재하지 않는 사용자입니다.')
        return value


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
