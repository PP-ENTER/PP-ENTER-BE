from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("facechats/", include("facechats.urls")),
    path("posts/", include("posts.urls")),
    path("accounts/", include("accounts.urls")),
]
