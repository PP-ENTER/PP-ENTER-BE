from django.conf import settings
from django.db import models
# from facechats.models import FaceChat

class Photo(models.Model):
    # photo_id = models.AutoField(primary_key=True) # Django는 기본적으로 id필드를 자동으로 추가하여 자동으로 값이 증가 -> 만약 사용자 정의로 필드명을 작성하면 해당 내용처럼 필드명을 작성하고 이렇게 되면 장고는 id값을 자동으로 생성하지x
    photo_name = models.TextField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_user') # CustomUser.id(o), CustomUser.user_id(x)
    face_chat_id = models.ForeignKey('facechats.FaceChat', on_delete=models.CASCADE, related_name='posts_facechat') # facechats > models.py에서 posts의 Tag를 import하고 있기에 여기서 FaceChat 모델을 import하면 에러..
    image_url = models.ImageField(blank=True, null=True)
    content = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Like", related_name="liked_posts")
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f"{self.user_id}'s post ({self.created_at})"


class Like(models.Model):
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes_photo')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('photo_id', 'user_id')


class Favorite(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='favorites_photo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'photo_id')


class Comment(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments_photo')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 대댓글을 위한 self-referential ForeignKey
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


class Tag(models.Model):
    # tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    
class PhotoTag(models.Model):
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_tags')
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        unique_together = ('photo_id', 'tag_id')