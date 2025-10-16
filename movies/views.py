from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .tmdb import get_rows, search_movies, movie_detail
from .models import Movie, Profile
from .models import Movie, Profile, Watch   # Watch must exist in models.py
import requests

def _active_profile(request):
    """Return the currently selected profile (if any)."""
    pid = request.session.get("active_profile_id")
    if request.user.is_authenticated and pid:
        try:
            return Profile.objects.get(id=pid, user=request.user)
        except Profile.DoesNotExist:
            return None
    return None

@login_required
def home(request):
    """Home/Browse page with horizontal rows (Trending, Top Rated, etc.)."""
    rows = {}
    import requests
    for label, url in get_rows().items():
        rows[label] = requests.get(url).json().get("results", [])[:18]
    return render(request, "movies/home.html", {"rows": rows, "profile": _active_profile(request)})

@login_required
def search(request):
    q = request.GET.get("q", "")
    results = search_movies(q) if q else []
    return render(request, "movies/search.html", {"q": q, "results": results})

@login_required
def detail(request, tmdb_id):
    data, key = movie_detail(tmdb_id)
    prof = _active_profile(request)
    in_list = prof.my_list.filter(tmdb_id=tmdb_id).exists() if prof else False
    return render(request, "movies/detail.html", {"m": data, "yt": key, "in_list": in_list})

@login_required
def toggle_list(request, tmdb_id):
    prof = _active_profile(request)
    if not prof:
        return redirect("profiles")
    data, key = movie_detail(tmdb_id)
    movie, _ = Movie.objects.get_or_create(
        tmdb_id=tmdb_id,
        defaults={
            "title": data.get("title", ""),
            "overview": data.get("overview", ""),
            "poster_path": data.get("poster_path", ""),
            "backdrop_path": data.get("backdrop_path", ""),
            "trailer_youtube_key": key,
        },
    )
    if prof.my_list.filter(tmdb_id=tmdb_id).exists():
        prof.my_list.remove(movie)
    else:
        prof.my_list.add(movie)
    return redirect("movie_detail", tmdb_id=tmdb_id)
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def watch(request, tmdb_id):
    """Log that the user started watching, then redirect to YouTube trailer (if available)."""
    profile = _active_profile(request)
    if not profile:
        return redirect("profiles")

    # ensure Movie exists locally
    data, key = movie_detail(tmdb_id)
    movie, _ = Movie.objects.get_or_create(
        tmdb_id=tmdb_id,
        defaults={
            "title": data.get("title", ""),
            "overview": data.get("overview", ""),
            "poster_path": data.get("poster_path", ""),
            "backdrop_path": data.get("backdrop_path", ""),
            "trailer_youtube_key": key,
        },
    )

    # create/update a watch row (simple: set seconds=1)
    Watch.objects.update_or_create(
        profile=profile, movie=movie,
        defaults={"seconds": 1, "finished": False}
    )

    # redirect to trailer if we have it; else stay on detail
    if key:
        return HttpResponseRedirect(f"https://www.youtube.com/watch?v={key}")
    return redirect("movie_detail", tmdb_id=tmdb_id)

@login_required
def mark_finished(request, tmdb_id):
    """Mark a title as finished so it disappears from Continue Watching."""
    profile = _active_profile(request)
    if not profile:
        return redirect("profiles")
    try:
        movie = Movie.objects.get(tmdb_id=tmdb_id)
        Watch.objects.filter(profile=profile, movie=movie).update(finished=True)
    except Movie.DoesNotExist:
        pass
    return redirect("movie_detail", tmdb_id=tmdb_id)
