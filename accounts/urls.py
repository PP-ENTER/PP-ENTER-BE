from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserUpdateView,
    FriendRequestView,
    ProfileView,
    FriendListView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
]