from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Friend, FriendRequest
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserUpdateSerializer,
    FriendSerializer,
    FriendRequestSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": serializer.data,
            "message": "사용자 생성이 완료되었습니다. 이제 로그인하세요."
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response(token, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.perform_update(serializer)
        return Response(serializer.data)


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.perform_update(serializer)
        return Response(serializer.data)


class FriendList(generics.ListCreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FriendDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer


class FriendRequestList(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class FriendRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get('status') == FriendRequest.ACCEPTED:
            from_user = instance.from_user
            to_user = instance.to_user

            # 양방향 친구 관계 생성
            Friend.objects.create(user=from_user, friend=[to_user])
            Friend.objects.create(user=to_user, friend=[from_user])

            # 친구 요청 삭제
            instance.delete()

            return Response({'detail': '친구 요청이 수락되었습니다.'}, status=status.HTTP_200_OK)

        self.perform_update(serializer)
        return Response(serializer.data)
