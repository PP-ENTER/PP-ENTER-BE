from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=255, unique=False)  # 닉네임
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)  # 프로필 이미지
    updated_at = models.DateTimeField(auto_now=True)  # 수정일



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)  # CustomUser와 1:1 관계
    # primary_key를 CustomUser의 pk로 설정하여 통합적으로 관리
    nickname = models.CharField(max_length=255, unique=False)  # 닉네임
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)  # 프로필 이미지
    first_name = models.CharField(max_length=255, null=True, blank=True)  # 이름
    last_name = models.CharField(max_length=255, null=True, blank=True)  # 성
    updated_at = models.DateTimeField(auto_now=True)  # 수정일

    def __str__(self):
        return self.nickname


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, nickname=instance.nickname, profile_image=instance.profile_image,
                                first_name=instance.first_name, last_name=instance.last_name)
        # CustomUser가 생성되면 Profile도 생성되도록 함


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