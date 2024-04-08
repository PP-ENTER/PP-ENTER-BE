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
    path('friend/', FriendList.as_view(), name='friend-list'),
    path('friend/<int:pk>/', FriendDetail.as_view(), name='friend-detail'),
    path('friend-request/', FriendRequestList.as_view(), name='friend-request-list'),
    path('friend-request/<int:pk>/', FriendRequestDetail.as_view(), name='friend-request-detail'),
]