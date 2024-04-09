from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CustomUser, Profile, Friend, FriendRequest

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            nickname='testnickname',
            profile_image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpg'),
            first_name='testfirst',
            last_name='testlast'
        )

    def test_create_custom_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.nickname, 'testnickname')
        self.assertEqual(self.user.profile_image.url, '/media/profile/test_image.jpg')
        self.assertEqual(self.user.first_name, 'testfirst')
        self.assertEqual(self.user.last_name, 'testlast')

    def test_create_profile(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.nickname, 'testnickname')
        self.assertEqual(profile.profile_image.url, '/media/profile/test_image.jpg')
        self.assertEqual(profile.first_name, 'testfirst')
        self.assertEqual(profile.last_name, 'testlast')

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            username='testsuperuser',
            password='testpassword',
            nickname='testsupernickname',
            profile_image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpg'),
            first_name='testsuperfirst',
            last_name='testsuperlast'
        )
        self.assertEqual(superuser.username, 'testsuperuser')
        self.assertEqual(superuser.nickname, 'testsupernickname')
        self.assertEqual(superuser.profile_image.url, '/media/profile/test_image.jpg')
        self.assertEqual(superuser.first_name, 'testsuperfirst')
        self.assertEqual(superuser.last_name, 'testsuperlast')


class FriendTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='testuser1',
            password='testpassword1',
            nickname='testnickname1',
            first_name='testfirst1',
            last_name='testlast1'
        )
        self.user2 = CustomUser.objects.create_user(
            username='testuser2',
            password='testpassword2',
            nickname='testnickname2',
            first_name='testfirst2',
            last_name='testlast2'
        )

    def test_friend_request_create(self):
        friend_request  = FriendRequest.objects.create(
            from_user=self.user1,
            to_user=self.user2
        )
        self.assertEqual(friend_request.from_user, self.user1)
        self.assertEqual(friend_request.to_user, self.user2)
        self.assertFalse(friend_request.status)

    def test_friend_create(self):
        friend = Friend.objects.create(
            user=self.user1,
            friend=self.user2
        )
        self.assertEqual(friend.user, self.user1)
        self.assertEqual(friend.friend, self.user2)

    def test_unique_friend(self):
        with self.assertRaises(Exception):
            Friend.objects.create(user=self.user1, friend=self.user2)

    def test_friend_str(self):
        self.assertEqual(str(self.friend), 'testnickname1 : testnickname2')
