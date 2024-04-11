from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Photo, Like, Favorite, Comment, Tag, PhotoTag
from .serializers import (
    PostSerializer, LikeSerializer, FavoriteSerializer,
    CommentSerializer, TagSerializer, PhotoTagSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user


class PostListView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PostSerializer

class PostCreateView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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
        serializer.save(user=self.request.user, photo=photo, parent_id=self.request.data.get('parent_id'))


class CommentUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagSearchView(generics.ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return Tag.objects.filter(name__icontains=query)


class TagDestroyView(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class PhotoTagCreateView(generics.CreateAPIView):
    queryset = PhotoTag.objects.all()
    serializer_class = PhotoTagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class PhotoTagDestroyView(generics.DestroyAPIView):
    queryset = PhotoTag.objects.all()
    serializer_class = PhotoTagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


