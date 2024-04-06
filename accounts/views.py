from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
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
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        username = serializer.validated_data['username']
        nickname = serializer.validated_data['nickname']
        password = serializer.validated_data['password']
        profile_image = serializer.validated_data.get('profile_image', None)
        first_name = serializer.validated_data.get('first_name', None)
        last_name = serializer.validated_data.get('last_name', None)

        user = User.objects.create_user(
            username=username,
            nickname=nickname,
            password=password,
            profile_image=profile_image,
            first_name=first_name,
            last_name=last_name
        )
        return user


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data['username'])
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # login(request, user)
            # return Response(serializer.data, status=status.HTTP_200_OK)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': '존재하지 않는 사용자입니다.'}, status=status.HTTP_404_NOT_FOUND)

            if not user.check_password(password):
                return Response({'error': '잘못된 비밀번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            data = {
                'id': user.id,
                'nickname': user.nickname,
                'access_token': access
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
