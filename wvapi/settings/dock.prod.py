import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST","")# "sisitech.com"
EMAIL_HOST_USER =  os.getenv("EMAIL_HOST_USER","")# "apitz@sisitech.com"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD","")# "tatawauwzniurpsh"

SMTP_PORT = int(os.getenv("SMTP_PORT","587"))

DEFAULT_FROM_EMAIL =  os.getenv("DEFAULT_FROM_EMAIL") 


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "memcached:11211",
    }
}
CACHE_TIMEOUT = 60 * 8



STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "../../templates"),)
CORS_ORIGIN_ALLOW_ALL = True

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# DEBUG=True




