import os, requests

API = "https://api.themoviedb.org/3"
KEY = os.getenv("TMDB_API_KEY")  # reads from .env

def get_rows():
    """Endpoints for rows on the home page."""
    return {
        "Trending": f"{API}/trending/movie/week?api_key={KEY}",
        "Top Rated": f"{API}/movie/top_rated?api_key={KEY}",
        "Action": f"{API}/discover/movie?api_key={KEY}&with_genres=28",
        "Comedy": f"{API}/discover/movie?api_key={KEY}&with_genres=35",
        "Horror": f"{API}/discover/movie?api_key={KEY}&with_genres=27",
    }

def search_movies(q):
    """Search movies by text."""
    return requests.get(f"{API}/search/movie?api_key={KEY}&query={q}").json().get("results", [])

def movie_detail(tmdb_id):
    """Single movie + trailer key (if any)."""
    detail = requests.get(
        f"{API}/movie/{tmdb_id}?api_key={KEY}&append_to_response=videos"
    ).json()
    key = ""
    for v in detail.get("videos", {}).get("results", []):
        if v.get("site") == "YouTube" and v.get("type") == "Trailer":
            key = v.get("key"); break
    return detail, key
