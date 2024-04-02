from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    user_no = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255)
    
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['username', 'email']

class Friend(models.Model):
    user_no = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend_no = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
