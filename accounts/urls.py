from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("profiles/", views.profile_select, name="profiles"),
    path("profiles/create/", views.profile_create, name="profile_create"),
    path("profiles/use/<int:pk>/", views.use_profile, name="use_profile"),
]
