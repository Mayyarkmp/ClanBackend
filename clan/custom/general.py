import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv()

DEBUG = True
APP_SCHEME = ""
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-lz3a&twztkdv2dq5q*4jq^g*j^mp#3kt*qj_@!8**kgkoqlinb"
)
ALLOWED_HOSTS = ["*"]  # ["134.122.80.7", "clan.sa", "localhost", "backend.clan.sa"]
AUTH_USER_MODEL = "users.User"
WSGI_APPLICATION = "clan.wsgi.application"
ASGI_APPLICATION = "clan.asgi.application"
ROOT_URLCONF = "clan.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1


SOFT_DELETE = True
handler404 = "core.views.custom_404"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "clan.middlewares.language.LanguageMiddleware",
    "clan.middlewares.session.EnsureSessionMiddleware",
]


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL_CACHE", "redis://localhost:6379/4"),
        "TIMEOUT": 6,
    }
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


SWAGGER_SETTINGS = {
    # 'SECURITY_DEFINITIONS': {
    #     'Bearer': {
    #         'type': 'apiKey',
    #         'name': 'Authorization',
    #         'in': 'header'
    #     }
    # }
}

USER_AGENTS_CACHE = "default"

if os.getenv("ENV") == "development":
    CORS_ALLOW_ALL_ORIGINS = True

else:
    CORS_ALLOWED_ORIGINS = [
        "http://clan.sa",
        "https://clan.sa",
        "http://dashboard.clan.sa",
        "https://dashboard.clan.sa",
        "http://backend.clan.sa",
        "https://backend.clan.sa",
        "http://localhost:3000",
    ]
