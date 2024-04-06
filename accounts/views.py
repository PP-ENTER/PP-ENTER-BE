from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate, login
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
        try:
            to_user = User.objects.get(id=request.data['to_user'])
        except User.DoesNotExist:
            return Response({'message': '존재하지 않는 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)
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
        return Friend.objects.filter(user_id=self.request.to_user)
