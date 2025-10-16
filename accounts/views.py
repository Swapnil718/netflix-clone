from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from movies.models import Profile

def signup_view(request):
    if request.method == "POST":
        email = request.POST["email"].strip()
        password = request.POST["password"]
        if not email or not password:
            return render(request, "accounts/signup.html", {"error": "Email and password required."})
        if User.objects.filter(username=email).exists():
            return render(request, "accounts/signup.html", {"error": "Account already exists. Try login."})
        user = User.objects.create_user(username=email, email=email, password=password)
        Profile.objects.create(user=user, name="Me", avatar="🙂")
        login(request, user)
        return redirect("profiles")
    return render(request, "accounts/signup.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"].strip()
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("profiles")
        return render(request, "accounts/login.html", {"error": "Invalid credentials."})
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def profile_select(request):
    if not request.user.is_authenticated:
        return redirect("login")
    profiles = Profile.objects.filter(user=request.user)
    return render(request, "accounts/profiles.html", {"profiles": profiles})

def profile_create(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        name = request.POST.get("name", "Me").strip() or "Me"
        avatar = request.POST.get("avatar", "🙂")
        Profile.objects.create(user=request.user, name=name, avatar=avatar)
        return redirect("profiles")
    return render(request, "accounts/profile_create.html")

def use_profile(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    prof = get_object_or_404(Profile, pk=pk, user=request.user)
    request.session["active_profile_id"] = prof.id
    return redirect("home")
