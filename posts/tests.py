# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.contrib.admin.sites import AdminSite
# from facechats.models import FaceChat
# from .models import Photo, Like, Favorite, Comment, Tag, PhotoTag
#
# class PhotoModelTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             password='testpass'
#         )
#         self.host = get_user_model().objects.create_user(
#             username='testhost',
#             password='testpass'
#         )
#         self.face_chat = FaceChat.objects.create(host_id=self.host)
#         self.photo = Photo.objects.create(
#             photo_name='Test Photo',
#             user_id=self.user,
#             face_chat_id=self.face_chat,
#             content='Test content'
#         )
#
#     def test_photo_creation(self):
#         self.assertEqual(self.photo.photo_name, 'Test Photo')
#         self.assertEqual(self.photo.user_id, self.user)
#         self.assertEqual(self.photo.face_chat_id, self.face_chat)
#         self.assertEqual(self.photo.content, 'Test content')
#
#     def test_photo_like(self):
#         like = Like.objects.create(photo_id=self.photo, user_id=self.user)
#         self.assertEqual(like.photo_id, self.photo)
#         self.assertEqual(like.user_id, self.user)
#
#     def test_photo_favorite(self):
#         favorite = Favorite.objects.create(photo_id=self.photo, user_id=self.user)
#         self.assertEqual(favorite.photo_id, self.photo)
#         self.assertEqual(favorite.user_id, self.user)
#
#     def test_photo_comment(self):
#         comment = Comment.objects.create(
#             photo_id=self.photo,
#             user_id=self.user,
#             content='Test comment'
#         )
#         self.assertEqual(comment.photo_id, self.photo)
#         self.assertEqual(comment.user_id, self.user)
#         self.assertEqual(comment.content, 'Test comment')
#
#     def test_photo_tag(self):
#         tag = Tag.objects.create(name='Test Tag')
#         photo_tag = PhotoTag.objects.create(photo_id=self.photo, tag_id=tag)
#         self.assertEqual(photo_tag.photo_id, self.photo)
#         self.assertEqual(photo_tag.tag_id, tag)
