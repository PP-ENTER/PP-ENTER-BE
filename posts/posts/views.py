from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Photo, Like, Favorite, Comment, Tag, PhotoTag
from .serializers import (
    PhotoSerializer, LikeSerializer, FavoriteSerializer,
    CommentSerializer, TagSerializer, PhotoTagSerializer
)

class PhotoListCreateView(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class PhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

class LikeDestroyView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class FavoriteCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

class FavoriteDestroyView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        photo_id = self.kwargs.get('photo_id')
        photo = Photo.objects.get(id=photo_id)
        serializer.save(user_id=self.request.user, photo_id=photo)

class CommentUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

class PhotoTagCreateView(generics.CreateAPIView):
    queryset = PhotoTag.objects.all()
    serializer_class = PhotoTagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class PhotoTagDestroyView(generics.DestroyAPIView):
    queryset = PhotoTag.objects.all()
    serializer_class = PhotoTagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user