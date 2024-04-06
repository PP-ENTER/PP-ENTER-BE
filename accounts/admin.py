from django.contrib import admin
from .models import CustomUser, Friend, FriendRequest

admin.site.register(CustomUser)
admin.site.register(Friend)
admin.site.register(FriendRequest)
