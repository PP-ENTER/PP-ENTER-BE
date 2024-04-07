from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CustomUser, Profile, Friend, FriendRequest

class CustomUserTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            nickname='testnickname',
            profile_image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpg'),
            first_name='testfirst',
            last_name='testlast'
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.nickname, 'testnickname')
        self.assertEqual(self.user.profile_image.url, '/media/profile/test_image.jpg')
        self.assertEqual(self.user.first_name, 'testfirst')
        self.assertEqual(self.user.last_name, 'testlast')

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
