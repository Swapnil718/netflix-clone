## Netflix Clone (Django + Tailwind + TMDB)

A portfolio-ready, Netflix-style web app built with Django, Tailwind CSS, and the TMDB API. It supports multi-profile accounts, browse rows (Trending/Top Rated/Genres), search, movie detail, trailers, My List, and Continue Watching.

Educational project — metadata/posters provided by TMDB
. This product uses the TMDB API but is not endorsed or certified by TMDB.

--
## ✨ Features

Auth & Profiles: Email/password auth, multi-profile per account, per-profile session.

Home/Browse: Horizontal carousels for Trending, Top Rated, Action, Comedy, Horror.

Search: Query TMDB; results link to detail pages.

Detail Page: Poster/backdrop, overview, trailer link (YouTube), Add/Remove My List.

My List: Personal watchlist persisted per profile.

Continue Watching: Tracks partial viewing and shows a prioritized row on Home.

Responsive UI: Clean dark theme with HTML.

---
🧱 Tech Stack

Backend: Django 5, SQLite (dev)

Frontend: Django templates, Tailwind CSS (CDN for dev)

Data: TMDB REST API (v3), YouTube trailers (redirect)

Python deps: django, requests, python-dotenv

📂 Project Structure
netflix_clone/
├─ core/
│  ├─ settings.py
│  └─ urls.py
├─ movies/
│  ├─ models.py      # Movie, Profile, Watch
│  ├─ views.py       # home/search/detail/toggle_list/watch/mark_finished
│  ├─ tmdb.py        # TMDB helpers: get_rows/search/detail
│  └─ urls.py
├─ accounts/
│  ├─ views.py       # login/signup/logout/profile select/create/use
│  └─ urls.py
├─ templates/
│  ├─ base.html
│  ├─ movies/
│  │  ├─ home.html
│  │  ├─ detail.html
│  │  └─ search.html
│  └─ accounts/
│     ├─ login.html
│     ├─ signup.html
│     ├─ profiles.html
│     └─ profile_create.html
├─ static/
├─ manage.py
└─ .env              # your secrets (not committed)

🚀 Getting Started
1) Prereqs

Python 3.10+

(Optional) Node.js if you later switch from Tailwind CDN to a build.

2) Clone
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

3) Virtual env & Install

Windows (PowerShell):

python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt  # or: pip install django requests python-dotenv


macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or: pip install django requests python-dotenv


If you don’t have a requirements.txt, create one:

Django>=5.0
requests
python-dotenv

4) Environment Variables

Create .env in the project root (same level as manage.py):

DEBUG=True
SECRET_KEY=dev-secret-change-me
TMDB_API_KEY=YOUR_TMDB_V3_API_KEY
ALLOWED_HOSTS=127.0.0.1,localhost


Get a free TMDB v3 API key:
TMDB → Settings → API → request a Developer key → copy API Key (v3 auth).

5) Migrate & Run
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


Open: http://127.0.0.1:8000

6) First-time Flow

Sign up (Accounts → Sign up)

Create/select a Profile

Browse Home rows, click a poster → Detail

Play Trailer (YouTube) or + My List

Use the header Search box

🧠 Core Models (simplified)

Movie: tmdb_id, title, overview, poster_path, backdrop_path, trailer_youtube_key

Profile: user, name, avatar, my_list (ManyToMany → Movie)

Watch: profile, movie, seconds, finished, updated_at

Drives the Continue Watching row (unfinished, most recent first)

🔌 TMDB Integration

Home rows: trending/top-rated/genres from TMDB endpoints

Search: GET /search/movie?query=...

Detail: GET /movie/{id}?append_to_response=videos (to extract YouTube trailer key)

Images: Posters/backdrops via TMDB CDN (e.g., https://image.tmdb.org/t/p/w300...)

🧭 Key Views & Routes

/ → Home (rows + optional My List and Continue Watching at top)

/movies/<tmdb_id>/ → Detail

/movies/search/?q=... → Search

/movies/toggle-list/<tmdb_id>/ → Add/Remove My List

/movies/watch/<tmdb_id>/ → Log watch & redirect to trailer

/movies/finish/<tmdb_id>/ → Mark finished (removes from Continue Watching)

/accounts/login|signup|logout|profiles|profiles/create|profiles/use/<id>/

🛠️ Development Notes

Tailwind: Using CDN in base.html for simplicity. Swap to a build when deploying.

Settings: .env loaded via python-dotenv.

Auth: Django’s built-in auth; email used as username for simplicity.

Profiles: Active profile stored in session to scope My List & Watch state.

Continue Watching: Created/updated on “Play Trailer”. You can wire to a real player later.

🧩 Troubleshooting

No rows on home → Check .env has valid TMDB_API_KEY; restart server.

Tailwind styles missing → Ensure the CDN <script src="https://cdn.tailwindcss.com"></script> is in base.html.

Profile loop → After signup, go to Profiles and click a profile to set it active.

favicon 404 → Add a tiny icon at static/favicon.ico and link it in base.html.

🗺️ Roadmap (nice-to-haves)

Proper Tailwind build (PostCSS/Vite) + component library

Real video player + playback position

Pagination & infinite scroll

Postgres + Docker + deployment (Render/Fly/Heroku)

Unit tests for views/models (pytest + coverage)

🤝 Acknowledgments

TMDB for movie data and images.

YouTube for trailer playback.

📜 License

MIT — see LICENSE (add one if this is public).

📸 Screenshots (placeholders)

Add images (or GIFs) to help reviewers:

/assets/screenshot-home.png
/assets/screenshot-detail.png
/assets/screenshot-profiles.png


Example in README:

![Home](assets/screenshot-home.png)
![Detail](assets/screenshot-detail.png)
![Profiles](assets/screenshot-profiles.png)
