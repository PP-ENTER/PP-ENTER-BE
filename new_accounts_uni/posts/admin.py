from django.contrib import admin
from .models import Post, Like, Favorite, Comment, Tag, PhotoTag

# 관리자 페이지에서 모델 데이터를 보기 좋게 표시하기 위한 클래스
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'content', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content', 'user_id', 'photo_tag')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'photo')

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'photo')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content')

admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
admin.site.register(PhotoTag)