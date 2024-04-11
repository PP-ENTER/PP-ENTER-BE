from django.urls import path
from .views import (
    PhotoListCreateView, PhotoRetrieveUpdateDeleteView,
    LikeCreateView, LikeDeleteView,
    FavoriteCreateView, FavoriteDeleteView,
    CommentCreateView, CommentUpdateDeleteView,
    TagListCreateView, PhotoTagCreateView, PhotoTagDeleteView
)

app_name = 'posts'

urlpatterns = [
    path('photos/', PhotoListCreateView.as_view(), name='photo_list_create'),
    path('photos/<int:pk>/', PhotoRetrieveUpdateDeleteView.as_view(), name='photo_detail'),
    path('likes/', LikeCreateView.as_view(), name='like_create'),
    path('likes/<int:pk>/', LikeDeleteView.as_view(), name='like_delete'),
    path('favorites/', FavoriteCreateView.as_view(), name='favorite_create'),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite_delete'),
    path('comments/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/', CommentUpdateDeleteView.as_view(), name='comment_update_delete'),
    path('tags/', TagListCreateView.as_view(), name='tag_list_create'),
    path('photo_tags/', PhotoTagCreateView.as_view(), name='photo_tag_create'),
    path('photo_tags/<int:pk>/', PhotoTagDeleteView.as_view(), name='photo_tag_delete'), 
]
