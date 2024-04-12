from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.models import CustomUser
from django.conf import settings



class Notice(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notice_type = models.IntegerField() # 1:좋아요, 2:채팅방 3:친구요청 등
    related_id = models.IntegerField() # 댓글id, 채팅방id, 유저id 등
    content = models.TextField()
    is_read = models.BooleanField() # -> 유저가 알림을 읽었는지
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # unique_together = ("notice", "content")
        pass