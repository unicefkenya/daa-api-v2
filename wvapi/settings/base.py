"""
Django settings for template project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path

from dotenv import load_dotenv
dotenv_filepath = (Path(__file__).parent/ "../../.env").resolve()
load_dotenv(dotenv_filepath)

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

USE_X_FORWARDED_HOST = True


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


ALLOWED_HOSTS_STR = os.getenv("ALLOWED_HOSTS","*")

ALLOWED_HOSTS = list( map(lambda x:x.strip(),ALLOWED_HOSTS_STR.split(",")) ) 


##Logging user activity
ACTIVATE_LOGS = False
LOG_AUTHENTICATED_USERS_ONLY = False



MY_SITE_URL = ""

IP_ADDRESS_HEADERS = (
    "HTTP_X_REAL_IP",
    "HTTP_CLIENT_IP",
    "HTTP_X_FORWARDED_FOR",
    "REMOTE_ADDR",
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_filters",
    "corsheaders",
    "rest_framework",
    "social_django",
    "oauth2_provider",
    "rest_framework_social_oauth2",
    "background_task",
    "client",
    "school.apps.SchoolConfig",
    "drf_autodocs",
    "region",
    "multiselectfield",
    "attendance",
    "support_question.apps.SupportConfig",
    "stats.apps.StatsConfig",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "client.middleware.UserLoggerMiddleware",
]

LEARNER_MIN_AGE = 3
LEARNER_MAX_AGE = 30
ROOT_URLCONF = "wvapi.urls"


REST_FRAMEWORK = {"DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",)}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    # 'DATETIME_FORMAT': "%a, %d %b %y %I:%M %p"
}
OAUTH2_PROVIDER = {
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 60 * 60,
    "ACCESS_TOKEN_EXPIRE_SECONDS": 60 * 60 * 12 * 365 * 20,
}

AUTH_USER_MODEL = "client.MyUser"

WSGI_APPLICATION = "wvapi.wsgi.application"
MY_SITE_URL=""

CUSTOM_REPORTS = (("overall", "General Overall Report"),)


AUTHENTICATION_BACKENDS = (
    # Others auth providers (e.g. Google, OpenId, etc)
    # Facebook OAuth2
    "social_core.backends.facebook.FacebookAppOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
    # Google
    "social_core.backends.google.GooglePlusAuth",
    # 'social.backends.google.GoogleOAuth2'
    # django-rest-framework-social-oauth2
    "rest_framework_social_oauth2.backends.DjangoOAuth2",
    # Django
    "django.contrib.auth.backends.ModelBackend",
)



DOCS_TITLE = os.getenv("DOCS_TITLE","Digital Attendance Application Kenya") 
DOCS_SUB_TITLE = os.getenv("DOCS_SUB_TITLE", "API Endpoints")

DOCS_LOGO  = os.getenv("DOCS_LOGO", "https://onekana.naconek.ke/assets/images/kenya_logo.png")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "..", "templates"),
        ],
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
MYDJANGOFILTERBACKEND_EXCLUDED_FILTER_FIELDS = ("raw_data", "json")


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"

AUTH_USER_MODEL = "client.MyUser"

DEFAULT_FROM_EMAIL = "Onekana Digital Attendance <onekana@naconek.ke>"

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_L10N = True

USE_TZ = True

#


USE_S3 = os.getenv("USE_S3", "False")=="True"


if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID") # eg  
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") # 
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME") #
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME") # eg  #
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")# eg
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl":  f"max-age={int(os.getenv('AWS_S3_MAX_AGE','86400'))}",
    }

    AWS_STATIC_LOCATION = os.getenv("AWS_STATIC_LOCATION") # eg "static"
    STATIC_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STATIC_LOCATION)
    STATICFILES_STORAGE = "wvapi.storage.StaticStorage"
    

    AWS_MEDIA_LOCATION = os.getenv("AWS_MEDIA_LOCATION") # eg "media"
    MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_MEDIA_LOCATION)
    DEFAULT_FILE_STORAGE = "wvapi.storage.MediaStorage"

else:
    # STATIC_ROOT = os.path.join(BASE_DIR, "uploads")
    STATIC_ROOT = os.getenv("STATIC_ROOT","./test_static") 
    STATIC_URL = os.getenv("STATIC_URL","/static/")

    # MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
    MEDIA_ROOT = os.getenv("MEDIA_ROOT","./test_media") 
    MEDIA_URL = os.getenv("MEDIA_URL","/media/") 