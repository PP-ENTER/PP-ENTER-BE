from django.urls import path
from .views import (
    PostMainListView, PostDetailListView, PostMainListSearchView, PostDetailListSearchView
)

urlpatterns = [
    path('posts_main_list/', PostMainListView.as_view(), name='posts_main_list'),
    path('posts_detail_list/<int:userid>/', PostDetailListView.as_view(), name='posts_detail_list'),
    path('posts_main_list_search/<str:photo_name>/', PostMainListSearchView.as_view(), name='posts_main_list_search'),
    path('posts_detail_list_search/<str:photo_name>/', PostDetailListSearchView.as_view(), name='posts_detail_list_search'),
]
