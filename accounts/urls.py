from django.urls import path
from .views import (
    UserCreateView,
    UserLoginView,
    UserUpdateView,
    FriendRequestView,
    ProfileView,
    FriendListView,
)

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
]