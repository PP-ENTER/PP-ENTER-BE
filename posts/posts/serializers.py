# serializers.py : 장고 모델 데이터를 json 타입으로 바꿔주는 작업
# https://codemonkyu.tistory.com/entry/Djnago-Django-rest-framework-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-API-%EC%84%9C%EB%B2%84-%EB%A7%8C%EB%93%A4%EA%B8%B0


# 24.04.04 base.html 확인을 위해 미작성
# -> 작성 필요

from rest_framework import serializers
from .models import Comment, Post, Like


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_username", "text", "created_at"]
        read_only_fields = ["author", "author_username"]


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "caption",
            "image",
            "created_at",
            "comments",
            "likes_count",
            "is_liked",
        ]
        read_only_fields = ["author", "author_username", "likes_count", "is_liked"]

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Like.objects.filter(post=obj, user=user).exists()
        return False