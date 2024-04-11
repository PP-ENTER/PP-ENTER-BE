from django.urls import path
from .views import (
    PostMainListView, PostDetailListView
)

urlpatterns = [
    path('posts_main_list/', PostMainListView.as_view(), name='posts_main_list'),
    path('posts_detail_list/<int:userid>/', PostDetailListView.as_view(), name='posts_detail_list'),
]
