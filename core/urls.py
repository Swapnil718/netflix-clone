from django.contrib import admin
from django.urls import path, include
from movies.views import home  # ✅ use the home view from movies

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("movies/", include("movies.urls")),
    path("accounts/", include("accounts.urls")),
]
