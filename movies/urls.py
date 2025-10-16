from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("<int:tmdb_id>/", views.detail, name="movie_detail"),
    path("toggle-list/<int:tmdb_id>/", views.toggle_list, name="toggle_list"),
    path("watch/<int:tmdb_id>/", views.watch, name="watch"),                 
    path("finish/<int:tmdb_id>/", views.mark_finished, name="mark_finished") 
]
