from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=255, unique=False)  # 닉네임
    profile_image = models.ImageField(
        upload_to="profile/", null=True, blank=True
    )  # 프로필 이미지
    is_active = models.BooleanField(default=True)  # 현재 접속 여부
    updated_at = models.DateTimeField(auto_now=True)  # 수정일


class Friend(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'friend_id',)

    def __str__(self):
        return f"{self.user} : {self.friend}"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_friend_requests"
    )
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_friend_requests"
    )
    status = models.BooleanField(
        default=False
    )  # 현재 상태 -> False: 요청중, True: 수락
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "from_user_id",
            "to_user_id",
        )

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"
