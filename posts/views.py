from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Photo
from .serializers import (
    PostSerializer
)



class PostMainListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Photo.objects.all().order_by('-created_at')[:10]