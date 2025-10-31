


# """
# Django settings for deconest_backend project.
# """

# from pathlib import Path
# from datetime import timedelta
# from decouple import config
# import os

# # ---------------------------
# # BASE DIRECTORY
# # ---------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

# # ---------------------------
# # SECURITY
# # ---------------------------
# SECRET_KEY = config("SECRET_KEY")
# DEBUG = config("DEBUG", default=False, cast=bool)

# # For AWS production
# ALLOWED_HOSTS = config(
#     "ALLOWED_HOSTS",
#     default="127.0.0.1,localhost,65.2.57.57",
#     cast=lambda v: [s.strip() for s in v.split(',')]
# )

# # ---------------------------
# # INSTALLED APPS
# # ---------------------------
# INSTALLED_APPS = [
#     # Default Django apps
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     # Third-party
#     'rest_framework',
#     'corsheaders',
#     'rest_framework_simplejwt.token_blacklist',

#     # DecoNest apps
#     'users.apps.UsersConfig',
#     'products',
#     'cart',
#     'wishlist',
#     'orders',
#     'adminpanel',
# ]

# # ---------------------------
# # RAZORPAY PAYMENT INTEGRATION
# # ---------------------------
# RAZORPAY_KEY_ID = config("RAZORPAY_KEY_ID")
# RAZORPAY_KEY_SECRET = config("RAZORPAY_KEY_SECRET")
# RAZORPAY_CURRENCY = config("RAZORPAY_CURRENCY", default="INR")

# # ---------------------------
# # REST FRAMEWORK & JWT CONFIG
# # ---------------------------
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.AllowAny',
#     ),
# }

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
# }

# # ---------------------------
# # CORS CONFIG
# # ---------------------------
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "http://localhost:5175",
#     "http://65.2.57.57",  # Allow your production frontend
# ]

# # Optional fallback during development
# CORS_ALLOW_ALL_ORIGINS = DEBUG

# AUTH_USER_MODEL = 'users.User'

# # ---------------------------
# # MIDDLEWARE
# # ---------------------------
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'deconest_backend.urls'

# # ---------------------------
# # TEMPLATES
# # ---------------------------
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'deconest_backend.wsgi.application'

# # ---------------------------
# # EMAIL CONFIGURATION
# # ---------------------------
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# # ---------------------------
# # DATABASE (PostgreSQL)
# # ---------------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }

# # ---------------------------
# # PASSWORD VALIDATORS
# # ---------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # ---------------------------
# # INTERNATIONALIZATION
# # ---------------------------
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # ---------------------------
# # STATIC & MEDIA FILES
# # ---------------------------
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / "static"]  # Development
# STATIC_ROOT = BASE_DIR / "staticfiles"    # Used for collectstatic

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# # ---------------------------
# # DEFAULT PRIMARY KEY
# # ---------------------------
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # ---------------------------
# # SECURITY HEADERS (Production)
# # ---------------------------
# if not DEBUG:
#     CSRF_COOKIE_SECURE = True
#     SESSION_COOKIE_SECURE = True
#     SECURE_BROWSER_XSS_FILTER = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
#     SECURE_HSTS_SECONDS = 31536000  # 1 year
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
#     X_FRAME_OPTIONS = 'DENY'



from pathlib import Path
from datetime import timedelta
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost,65.2.57.57,deconest-pearl.vercel.app",
    cast=lambda v: [s.strip() for s in v.split(',')]
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',

    'users.apps.UsersConfig',
    'products',
    'cart',
    'wishlist',
    'orders',
    'adminpanel',
]

RAZORPAY_KEY_ID = config("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = config("RAZORPAY_KEY_SECRET")
RAZORPAY_CURRENCY = config("RAZORPAY_CURRENCY", default="INR")

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ✅ CRITICAL FIX: Allow your Vercel frontend
CORS_ALLOWED_ORIGINS = [
    "https://deconest-pearl.vercel.app",
    "http://localhost:5173",
    "http://localhost:5175",
    "http://65.2.57.57",
]

# Optional fallback
CORS_ALLOW_ALL_ORIGINS = DEBUG

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'deconest_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deconest_backend.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'
