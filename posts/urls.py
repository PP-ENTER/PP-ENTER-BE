from django.urls import path
from .views import (
    PostMainListView,
)

urlpatterns = [
    path('posts_main_list/', PostMainListView.as_view(), name='posts_main_list'),
]
