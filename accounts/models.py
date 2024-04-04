from django.contrib.auth.models import AbstractUser
from django.db import models


AbstractUser
# id: 1
# username: 엄영철
# firstname: 영철(null)
# lastname: 엄(null)

# --------

# user_id : test / password test1234! => "로그인 정보"
# nickname : zerochul

class CustomUser(AbstractUser):
    # user_no = models.AutoField(primary_key=True) # 1, 2, 3,.... # 자동 증가(serialNo)
    user_id = models.CharField(max_length=255, unique=True)  # test, leehojun ..    # 고유한 사용자 ID 필드 추가
    nickname = models.CharField(max_length=255) # 별명
    profile_image = models.ImageField(upload_to="users/images/", null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True) # join date
    is_active = models.BooleanField(default=False) # 접속여부 
    updated_at = models.DateTimeField(auto_now=True)


class Friend(models.Model): 
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends')
    friend_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'friend_id',)

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_friend_requests')
    stauts = models.BooleanField() # 현재 상태 -> 1. 요청중, 거절, 2. 수락 => 상대방이 받으면 True -> Friend에 반영
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')