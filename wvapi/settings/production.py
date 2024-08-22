import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DEBUG = False
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": "moekeapi",  # Or path to database file if using sqlite3.
        "USER": "moeke",  # Not used with sqlite3.
        "PASSWORD": "VKMCrEDlMGYjSe3",  # Not used with sqlite3.
        "HOST": "db",  # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "16432" if "process_tasks" not in sys.argv else "5432",  # Set to empty string for default. Not used with sqlite3.
    }
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# DATABASES = {
#      'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'wvapi',        # Or path to database file if using sqlite3.
#         'USER': 'wvuser',                   # Not used with sqlite3.
#         'PASSWORD': '#wvuser',            # Not used with sqlite3.
#         'HOST': 'localhost',             # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '5432',                  # Set to empty string for default. Not used with sqlite3.
#     }
# }


# pg_dump -U nzmewqyrvjyhpl -h ec2-107-22-173-160.compute-1.amazonaws.com dcoimmfelmkfbc > winda_backup

# Update database configuration with $DATABASE_URL.
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allow all host headers
ALLOWED_HOSTS = ["*"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')


STATIC_ROOT = "/home/daa/apps/django/static/"
STATIC_URL = "/static/"

MEDIA_ROOT = "/home/daa/apps/django/media/"
MEDIA_URL = "/media/"

# Extra places for collectstatic to find static files.

# EMAIL_USE_SSL = True
# EMAIL_HOST="smtp.gmail.com"
# EMAIL_HOST_USER="sisitechdev@gmail.com"
# EMAIL_HOST_PASSWORD="#sisitech"
# EMAIL_PORT = 465


EMAIL_USE_TLS = True
EMAIL_HOST = "pld109.truehost.cloud"
EMAIL_HOST_USER = "onekana@naconek.ke"
EMAIL_HOST_PASSWORD = "NdUrpFStD7@J"

if "test" in sys.argv:
    STATIC_ROOT = "./test_static/"
    MEDIA_ROOT = "./test_media/"
    DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3", "NAME": "mydatabase"}


STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "../../templates"),)
CORS_ORIGIN_ALLOW_ALL = True
ADMINS = [
    ("Mwangi", "michameiu@gmail.com"),
]


SERVER_EMAIL = "onekana@naconek.ke"

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# DEBUG=True
