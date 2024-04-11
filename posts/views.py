from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Photo
from .serializers import (
    PostSerializer
)
from django.db.models import Q


class PostMainListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Photo.objects.all().order_by('-created_at')[:10]
    
class PostDetailListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('userid')
        if user_id == 0:  # '-1'이 전달되면 전체 포스트 목록 반환
            return Photo.objects.all().order_by('-created_at')
        else:  # 그렇지 않으면 해당 'userid'의 포스트만 필터링
            return Photo.objects.filter(author_id=user_id).order_by('-created_at')


class PostMainListSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
 
    def get_queryset(self):
        # photo_name = self.request.query_params.get('photo_name', None)
        photo_name = self.kwargs['photo_name']

        return Photo.objects.all().filter(Q(photo_name__icontains = photo_name)).order_by('-created_at')[:10]
    
class PostDetailListSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
 
    def get_queryset(self):
        # photo_name = self.request.query_params.get('photo_name', None)
        photo_name = self.kwargs['photo_name']

        return Photo.objects.all().filter(Q(photo_name__icontains = photo_name)).order_by('-created_at')