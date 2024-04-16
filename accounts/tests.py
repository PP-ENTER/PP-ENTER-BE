import random

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

from .models import CustomUser, Profile, Friend, FriendRequest
from .permissions import CustomReadOnly
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, FriendSerializer, FriendRequestSerializer

User = get_user_model()


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123!',
            nickname='testnickname',
            profile_image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpg'),
            first_name='testfirst',
            last_name='testlast'
        )

    def test_create_custom_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.nickname, 'testnickname')
        self.assertIsNotNone(self.user.profile_image)
        self.assertIsNotNone(self.user.first_name)
        self.assertIsNotNone(self.user.last_name)

    def test_create_profile(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.nickname, 'testnickname')
        self.assertIsNotNone(self.user.profile_image)
        self.assertIsNotNone(profile.first_name)
        self.assertIsNotNone(profile.last_name)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            username='testsuperuser',
            password='testpassword123!',
            email='test@example.com'
        )
        self.assertEqual(superuser.username, 'testsuperuser')
        self.assertEqual(superuser.email, 'test@example.com')


class FriendModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='testuser1', password='testpassword123!', nickname='Test User 1')
        self.user2 = User.objects.create(username='testuser2', password='testpassword123!', nickname='Test User 2')
        self.friend = Friend.objects.create(user=self.user1, friend=self.user2)

    def test_friend_creation(self):
        self.assertEqual(self.friend.user, self.user1)
        self.assertEqual(self.friend.friend, self.user2)
        self.assertIsNotNone(self.friend.created_at)
        self.assertEqual(str(self.friend), 'Test User 1 : Test User 2')

    def test_friend_request_create(self):
        friend_request = FriendRequest.objects.create(
            from_user=self.user1,
            to_user=self.user2
        )
        self.assertEqual(friend_request.from_user, self.user1)
        self.assertEqual(friend_request.to_user, self.user2)
        self.assertFalse(friend_request.status)

    def test_friend_create(self):
        friend1 = User.objects.create(username='friend1', password='friend1password', nickname='Friend 1')
        friend2 = User.objects.create(username='friend2', password='friend2password', nickname='Friend 2')
        friend = Friend.objects.create(user=friend1, friend=friend2)
        self.assertEqual(friend.user, friend1)
        self.assertEqual(friend.friend, friend2)

    def test_unique_friend(self):
        with self.assertRaises(Exception):
            Friend.objects.create(user=self.user1, friend=self.user2)

    def test_friend_str(self):
        self.assertEqual(str(self.friend), 'Test User 1 : Test User 2')


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123!')

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        expected_data = {
            'id': self.user.id,
            'username': 'testuser',
            'nickname': '',
            'profile_image': None,
            'first_name': '',
            'last_name': ''
        }
        self.assertEqual(serializer.data, expected_data)


class RegisterSerializerTestCase(TestCase):
    def test_register_serializer_valid(self):
        data = {
            'username': 'newuser',
            'nickname': 'New User',
            'password': 'newpassword123!',
            'password2': 'newpassword123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_register_serializer_invalid_password(self):
        data = {
            'username': 'newuser',
            'nickname': 'New User',
            'password': 'newpassword123!',
            'password2': 'differentpassword123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)


class LoginSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123!')

    def test_login_serializer_valid(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123!'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)

    def test_login_serializer_invalid(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class FriendSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpassword123!')
        self.user2 = User.objects.create_user(username='user2', password='testpassword123!')

    def test_friend_serializer_valid(self):
        data = {
            'user': self.user1.id,
            'friend': self.user2.id
        }
        serializer = FriendSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_friend_serializer_invalid_self_friend(self):
        data = {
            'user': self.user1.id,
            'friend': self.user1.id
        }
        serializer = FriendSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_friend_serializer_invalid_already_friends(self):
        Friend.objects.create(user=self.user1, friend=self.user2)
        Friend.objects.create(user=self.user2, friend=self.user1)

        data = {
            'user': self.user1.id,
            'friend': self.user2.id
        }
        serializer = FriendSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class FriendRequestSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpassword123!')
        self.user2 = User.objects.create_user(username='user2', password='testpassword123!')

    def test_friend_request_serializer_valid(self):
        data = {
            'from_user': self.user1.id,
            'to_user': self.user2.id
        }
        serializer = FriendRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_friend_request_serializer_invalid_self_request(self):
        data = {
            'from_user': self.user1.id,
            'to_user': self.user1.id
        }
        serializer = FriendRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class CustomReadOnlyPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.view = APIView()
        self.obj = self.user1  # 테스트용 객체 (예: 사용자 객체)

    def test_has_object_permission_safe_methods(self):
        request = self.factory.get('/')
        request.user = self.user1
        permission = CustomReadOnly()

        has_permission = permission.has_object_permission(request, self.view, self.obj)

        self.assertTrue(has_permission)

    def test_has_object_permission_unsafe_methods_owner(self):
        request = self.factory.post('/')
        request.user = self.user1
        permission = CustomReadOnly()

        has_permission = permission.has_object_permission(request, self.view, self.obj)

        self.assertTrue(has_permission)

    def test_has_object_permission_unsafe_methods_not_owner(self):
        request = self.factory.post('/')
        request.user = self.user2
        permission = CustomReadOnly()

        has_permission = permission.has_object_permission(request, self.view, self.obj)

        self.assertFalse(has_permission)


class URLPatternsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create_user(username='user1', password='password')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password')
        self.friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)

    def test_register_url(self):
        randnum = random.randint(100, 10000)
        url = reverse('register')
        data = {
            'username': 'new' + str(randnum),
            'password': 'password123!',
            'password2': 'password123!',
            'nickname': 'NewUser',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_url(self):
        url = reverse('user-login')
        data = {
            'username': 'user1',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_url(self):
        # 로그인 요청을 보내고 응답에서 리프레시 토큰 추출
        login_url = reverse('user-login')
        login_data = {
            'username': 'user1',
            'password': 'password'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']

        # 리프레시 토큰을 사용하여 토큰 리프레시 요청 보내기
        url = reverse('refresh')
        data = {
            'refresh': refresh_token
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_url(self):
        url = reverse('user-update')
        self.client.force_authenticate(user=self.user1)
        data = {
            'username': 'updateduser1'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_friend_request_url(self):
        url = reverse('accept-friend-request', args=[self.friend_request.id])
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_profile_url(self):
        url = reverse('profile')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_friend_list_url(self):
        url = reverse('friend-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'nickname': 'Test User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_view(self):
        randnum = random.randint(100, 10000)
        url = reverse('register')
        data = {
            'username': 'new' + str(randnum),
            'password': 'password123!',
            'password2': 'password123!',
            'nickname': 'NewUser',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login_view(self):
        url = reverse('user-login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile_view(self):
        url = reverse('profile')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_user_update_view(self):
        url = reverse('user-update')
        self.client.force_authenticate(user=self.user)
        data = {'nickname': 'Updated Nickname'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, 'Updated Nickname')


class FriendTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user'+str(random.randint(100, 10000)), password='password1')
        self.user2 = User.objects.create_user(username='user'+str(random.randint(100, 10000)), password='password2')

    def test_friend_request_view(self):
        # 기존 친구 요청 및 친구 관계 제거
        FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).delete()
        Friend.objects.filter(user=self.user1, friend=self.user2).delete()
        Friend.objects.filter(user=self.user2, friend=self.user1).delete()

        url = reverse('friend-request')
        self.client.force_authenticate(user=self.user1)
        data = {'from_user': self.user1.id,'to_user': self.user2.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FriendRequest.objects.count(), 1)

    def test_accept_friend_request_view(self):
        friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        url = reverse('accept-friend-request', kwargs={'friend_request_id': friend_request.id})
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friend.objects.count(), 2)
        self.assertEqual(FriendRequest.objects.count(), 0)

    def test_friend_view_get(self):
        Friend.objects.create(user=self.user1, friend=self.user2)
        Friend.objects.create(user=self.user2, friend=self.user1)
        url = reverse('friend-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_friend_view_post(self):
        # 기존 친구 관계 제거
        Friend.objects.filter(user=self.user1, friend=self.user2).delete()
        Friend.objects.filter(user=self.user2, friend=self.user1).delete()

        url = reverse('friend-list')
        self.client.force_authenticate(user=self.user1)
        data = {'user': self.user1.id, 'friend': self.user2.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friend.objects.count(), 2)
