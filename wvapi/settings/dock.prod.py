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
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": os.getenv("DB_NAME"),# "tzapi",  # Or path to database file if using sqlite3.
        "USER": os.getenv("DB_USER"),# "moeke",  # Not used with sqlite3.
        "PASSWORD":os.getenv("DB_PASSWORD"),# "VKMCrEDlMGYjSe3",  # Not used with sqlite3.
        "HOST":os.getenv("DB_HOST"),# "127.0.0.1",  # Set to empty string for localhost. Not used with sqlite3.
        "PORT": os.getenv("DB_PORT"),# "5432" if "process_tasks" not in sys.argv else "5432",  # Set to empty string for default. Not used with sqlite3.
    }
}

# DATABASES = {
#      'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'moekeapi',        # Or path to database file if using sqlite3.
#         'USER': 'moeke',                   # Not used with sqlite3.
#         'PASSWORD': 'VKMCrEDlMGYjSe3',            # Not used with sqlite3.
#         'HOST': 'onekana.naconek.ke',             # Set to empty string for localhost. Not used with sqlite3.
#         'PORT':'16432' if "process_tasks" not in sys.argv  else "5432",                  # Set to empty string for default. Not used with sqlite3.
#     }
# }

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


# Extra places for collectstatic to find static files.

# EMAIL_USE_SSL = True
# EMAIL_HOST="smtp.gmail.com"
# EMAIL_HOST_USER="sisitechdev@gmail.com"
# EMAIL_HOST_PASSWORD="#sisitech"
# EMAIL_PORT = 465


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


if "test" in sys.argv:
    STATIC_ROOT = "./test_static/"
    MEDIA_ROOT = "./test_media/"
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase",
    }


STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "../../templates"),)
CORS_ORIGIN_ALLOW_ALL = True

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# DEBUG=True


USE_S3 = os.getenv("USE_S3", "False")=="True"


if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID") # eg  "ADE24H4CX8MWW9D2LV"
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") # eg "1djabhiud78adadta768cponeEjG5fnUy2Do"
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME") # eg "onekanapi"
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME") # eg "fra1"  # replace with the region where your bucket is located
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")# eg "https://onekanapi.fra1.digitaloceanspaces.com"  # replace with the endpoint URL for your region
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl":  f"max-age={int(os.getenv('AWS_S3_MAX_AGE','86400'))}",
    }

    # DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
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


