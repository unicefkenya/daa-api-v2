import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DEBUG = False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2", 
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD":os.getenv("DB_PASSWORD"),
        "HOST":os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT",5432),
    }
}


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST","")
EMAIL_HOST_USER =  os.getenv("EMAIL_HOST_USER","")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD","")

SMTP_PORT = int(os.getenv("SMTP_PORT","587"))

DEFAULT_FROM_EMAIL =  os.getenv("DEFAULT_FROM_EMAIL") 




CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "memcached:11211",
    }
}
CACHE_TIMEOUT = 60 * 8


if "test" in sys.argv:
    STATIC_ROOT = "./test_static/"
    MEDIA_ROOT = "./test_media/"
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase",
    }


STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "../../templates"),)
CORS_ORIGIN_ALLOW_ALL = True




