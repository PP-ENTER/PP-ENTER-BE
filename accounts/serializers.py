import re

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import Friend, FriendRequest

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'profile_image', 'first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'profile_image', 'first_name', 'last_name')


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'nickname', 'password', 'password2', 'profile_image', 'first_name', 'last_name'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            profile_image=validated_data.get('profile_image', None),
            first_name=validated_data.get('first_name', None),
            last_name=validated_data.get('last_name', None)
        )

        user.set_password(validated_data['password'])
        user.save()

        refresh = RefreshToken.for_user(user)
        token = refresh.access_token

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            access_token = AccessToken.for_user(user)
            data['access'] = str(access_token)
            return data
        else:
            raise serializers.ValidationError('아이디 또는 비밀번호가 일치하지 않습니다.')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname', 'profile_image', 'first_name', 'last_name')


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('id', 'user', 'friend',)
        read_only_fields = ('id')

    def validate(self, data):
        user = data.get('user')
        friend = data.get('friend')

        if user == friend:
            raise serializers.ValidationError("Users cannot be friends with themselves.")

        if Friend.objects.filter(user=user, friend=friend).exists() or \
           Friend.objects.filter(user=friend, friend=user).exists():
            raise serializers.ValidationError("These users are already friends.")

        return data

    def create(self, validated_data):
        user = validated_data['user']
        friend = validated_data['friend']

        # Create the friendship in both directions
        Friend.objects.create(user=user, friend=friend)
        Friend.objects.create(user=friend, friend=user)

        return validated_data


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'created_at', 'status']
        read_only_fields = ['id']

    def validate(self, data):
        from_user = data.get('from_user')
        to_user = data.get('to_user')

        if from_user == to_user:
            raise serializers.ValidationError("Users cannot send friend requests to themselves.")

        return data
