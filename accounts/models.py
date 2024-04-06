from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=255, unique=True)  # 닉네임
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)  # 프로필 이미지
    updated_at = models.DateTimeField(auto_now=True)  # 수정일


class Friend(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend',)

    def __str__(self):
        return f'{self.user.nickname} : {self.friend.nickname}'


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.BooleanField(default=False)  # 현재 상태 -> False: 요청중, True: 수락
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user',)

    def __str__(self):
        return f'{self.from_user.nickname} -> {self.to_user.nickname}'