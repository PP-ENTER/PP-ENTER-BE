from django.urls import path
from .views import (
    CheckLoginView,
    LikeCreateView,
    LikeDestroyView,
    FavoriteCreateView,
    FavoriteDestroyView,
    CommentCreateView,
    CommentUpdateDestroyView,
    TagListCreateView,
    TagSearchView,
    TagDestroyView,
    PhotoTagCreateView,
    PhotoTagDestroyView,
    PostCreateView,
    PostListView,
    CheckLoginView,
    PostMainListView,
    PostDetailListView,
    PostDetailListSearchView,
    PostMainListSearchView,
    PostDetailView,
    PostDetailUpdateDelete,
)

app_name = "posts"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("<int:pk>/", PostDetailUpdateDelete.as_view(), name="post_update_delete"),
    path("likes/", LikeCreateView.as_view(), name="like_create"),
    path("likes/<int:pk>/", LikeDestroyView.as_view(), name="like_delete"),
    path("favorites/", FavoriteCreateView.as_view(), name="favorite_create"),
    path("favorites/<int:pk>/", FavoriteDestroyView.as_view(), name="favorite_delete"),
    path("comments/", CommentCreateView.as_view(), name="comment_create"),
    path(
        "comments/<int:pk>/",
        CommentUpdateDestroyView.as_view(),
        name="comment_update_delete",
    ),
    path("tags/", TagListCreateView.as_view(), name="tag_list_create"),
    path("tags/search/", TagSearchView.as_view(), name="tag-search"),
    path("tags/<int:pk>/", TagDestroyView.as_view(), name="tag_delete"),
    path("photo_tags/", PhotoTagCreateView.as_view(), name="photo_tag_create"),
    path(
        "photo_tags/<int:pk>/", PhotoTagDestroyView.as_view(), name="photo_tag_delete"
    ),
    path("posts_main_list/", PostMainListView.as_view(), name="posts_main_list"),
    path(
        "posts_detail_list/<int:userid>/",
        PostDetailListView.as_view(),
        name="posts_detail_list",
    ),
    path(
        "posts_main_list_search/<str:photo_name>/",
        PostMainListSearchView.as_view(),
        name="posts_main_list_search",
    ),
    path(
        "posts_detail_list_search/<str:photo_name>/",
        PostDetailListSearchView.as_view(),
        name="posts_detail_list_search",
    ),
    path("check-login/", CheckLoginView.as_view(), name="check_login"),
]
