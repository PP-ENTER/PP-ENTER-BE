from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Friend, FriendRequest, CustomUser

User = get_user_model()


admin.site.register(CustomUser)
admin.site.register(Friend)
admin.site.register(FriendRequest)
