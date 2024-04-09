from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserUpdateView,
    FriendList,
    FriendDetail,
    FriendRequestList,
    FriendRequestDetail,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-requests/<int:friend_request_id>/accept/',
         AcceptFriendRequestView.as_view(),
         name='accept-friend-request'
    ),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('friends/', FriendView.as_view(), name='friend-list'),
]