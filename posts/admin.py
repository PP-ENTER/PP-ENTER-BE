from django.contrib import admin
from .models import Photo, Like, Favorite, Comment, Tag, PhotoTag


admin.site.register(Photo)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(PhotoTag)
