import re

from rest_framework import serializers, status
from rest_framework.response import Response
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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    friend = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Friend
        fields = ['id', 'user', 'friend', 'created_at']

    def validate_friend(self, value):
        if self.context['request'].user in value:
            raise serializers.ValidationError('자기 자신을 친구로 추가할 수 없습니다.')

        return value

    def create(self, validated_data):
        friend = Friend.objects.create(
            user=validated_data['user']
        )
        friend.friend.add(*validated_data['friend'])
        return friend


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']

    def validate(self, data):
        if data['from_user'] == data['to_user']:
            raise serializers.ValidationError('자기 자신에게 친구 요청을 보낼 수 없습니다.')

        # 이미 친구 요청을 보낸 경우
        if FriendRequest.objects.filter(from_user=data['from_user'], to_user=data['to_user']).exists():
            raise serializers.ValidationError('이미 친구 요청을 보냈습니다.')

        # 이미 친구 요청을 받은 경우
        if FriendRequest.objects.filter(from_user=data['to_user'], to_user=data['from_user']).exists():
            raise serializers.ValidationError('상대방이 이미 친구 요청을 보냈습니다.')

        # 이미 친구인 경우
        if Friend.objects.filter(user=data['from_user'], friend=data['to_user']).exists() or Friend.objects.filter(
                user=data['to_user'], friend=data['from_user']).exists():
            raise serializers.ValidationError('이미 친구입니다.')

        return data

    def create(self, validated_data):
        friend_request = FriendRequest.objects.create(
            from_user=validated_data['from_user'],
            to_user=validated_data['to_user']
        )
        return friend_request
