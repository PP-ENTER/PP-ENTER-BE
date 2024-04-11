from django.urls import path
from .views import (
    PostListCreateView, PostRetrieveUpdateDestroyView,
    LikeCreateView, LikeDestroyView,
    FavoriteCreateView, FavoriteDestroyView,
    CommentCreateView, CommentUpdateDestroyView,
    TagListCreateView, PhotoTagCreateView, PhotoTagDestroyView
)

app_name = 'posts'

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post_detail'),
    path('likes/', LikeCreateView.as_view(), name='like_create'),
    path('likes/<int:pk>/', LikeDestroyView.as_view(), name='like_delete'),
    path('favorites/', FavoriteCreateView.as_view(), name='favorite_create'),
    path('favorites/<int:pk>/', FavoriteDestroyView.as_view(), name='favorite_delete'),
    path('comments/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/', CommentUpdateDestroyView.as_view(), name='comment_update_delete'),
    path('tags/', TagListCreateView.as_view(), name='tag_list_create'),
    path('photo_tags/', PhotoTagCreateView.as_view(), name='photo_tag_create'),
    path('photo_tags/<int:pk>/', PhotoTagDestroyView.as_view(), name='photo_tag_delete'), 
]
