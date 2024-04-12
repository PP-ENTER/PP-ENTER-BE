from django.urls import path
from . import views

urlpatterns = [
    path('', views.FaceChatList.as_view(), name='facechat_list'),
    path('<int:pk>/', views.FaceChatDetailView.as_view(), name='facechat_detail'),
    path('create_facechat/', views.FaceChatCreate.as_view(), name='facechat_create'),
]
