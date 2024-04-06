from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate, login
from .models import Friend, FriendRequest
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    FriendSerializer,
    FriendRequestSerializer,
    UserLoginSerializer,
)

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            return Response(user_data, status=status.HTTP_200_OK)
        return Response({'message': "로그인 실패", 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class FriendRequestView(APIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=to_user,
            status=False
        )
        if created:
            return Response({'message': '친구 요청 성공'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '이미 친구 요청을 보냈습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FriendListView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friend.objects.filter(user_id=self.request.user)
