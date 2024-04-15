from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Friend, FriendRequest, CustomUser
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserUpdateSerializer,
    FriendSerializer,
    FriendRequestSerializer,
    ProfileSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": serializer.data,
                "message": "사용자 생성이 완료되었습니다. 이제 로그인하세요.",
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]
        return Response(
            {
                "username": user.username,
                "nickname": user.nickname,
                "refresh": str(refresh),
                "access": str(access),
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # JWT 인증을 사용하는 경우 주석 해제

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FriendRequestView(generics.GenericAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_user = request.user
        to_user = serializer.validated_data["to_user"]

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response(
                {"detail": "Friend request already sent."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            Friend.objects.filter(user=from_user, friend=to_user).exists()
            or Friend.objects.filter(user=to_user, friend=from_user).exists()
        ):
            return Response(
                {"detail": "Users are already friends."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request = FriendRequest.objects.create(
            from_user=from_user, to_user=to_user
        )
        serializer = self.get_serializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AcceptFriendRequestView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, friend_request_id):
        try:
            friend_request = FriendRequest.objects.get(
                id=friend_request_id, to_user=request.user
            )
        except FriendRequest.DoesNotExist:
            return Response(
                {"detail": "Friend request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        from_user = friend_request.from_user
        to_user = friend_request.to_user

        # Create the friendship
        Friend.objects.create(user=from_user, friend=to_user)
        Friend.objects.create(user=to_user, friend=from_user)

        # Delete the friend request
        friend_request.delete()

        # Serialize the new friendship
        serializer = FriendSerializer(
            Friend.objects.get(user=from_user, friend=to_user)
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendView(generics.GenericAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = Friend.objects.filter(user=request.user)
        serializer = self.get_serializer(friends, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        friend = serializer.validated_data["friend"]

        if user == friend:
            return Response(
                {"detail": "Users cannot be friends with themselves."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            Friend.objects.filter(user=user, friend=friend).exists()
            or Friend.objects.filter(user=friend, friend=user).exists()
        ):
            return Response(
                {"detail": "Users are already friends."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Friend.objects.create(user=user, friend=friend)
        Friend.objects.create(user=friend, friend=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
