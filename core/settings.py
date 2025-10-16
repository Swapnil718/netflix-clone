import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

# --- Base ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security / env ---
SECRET_KEY = os.getenv("SECRET_KEY", "dev")  # set real one in Railway
DEBUG = os.getenv("DEBUG", "True") == "True"

# hosts & csrf (comma-separated in env)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
CSRF_TRUSTED_ORIGINS = (
    os.getenv("CSRF_TRUSTED_ORIGINS", "")
    .split(",")
    if os.getenv("CSRF_TRUSTED_ORIGINS")
    else []
)

# --- Apps ---
INSTALLED_APPS = [
    # WhiteNoise helper for dev (keeps static consistent with prod)
    "whitenoise.runserver_nostatic",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "movies",
    "accounts",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise must be right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# --- Database ---
# Default: sqlite for local dev
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# If Railway provides DATABASE_URL, switch to Postgres automatically
if os.getenv("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.parse(
        os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )

# --- Password validation (keep simple for demo) ---
AUTH_PASSWORD_VALIDATORS = []

# --- I18N ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files ---
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]      # your local /static
STATIC_ROOT = BASE_DIR / "staticfiles"        # where collectstatic puts files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Tell Django to serve gzip/brotli via WhiteNoise in prod
# (no extra settings needed beyond the storage + middleware)

# --- Security in prod behind proxy (Railway) ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "True") == "True"
SESSION_COOKIE_SECURE = COOKIE_SECURE
CSRF_COOKIE_SECURE = COOKIE_SECURE

# --- Auth redirects ---
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# --- External API keys ---
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
