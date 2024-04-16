from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    UserUpdateView,
    FriendRequestView,
    AcceptFriendRequestView,
    ProfileView,
    FriendView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("update/", UserUpdateView.as_view(), name="user-update"),
    path("friend-request/", FriendRequestView.as_view(), name="friend-request"),
    path(
        "friend-requests/<int:friend_request_id>/accept/",
        AcceptFriendRequestView.as_view(),
        name="accept-friend-request",
    ),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("friends/", FriendView.as_view(), name="friend-list"),
]
