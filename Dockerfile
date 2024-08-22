# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
from ubuntu:20.04

RUN apt update

RUN apt install -y python3-pip  git 
RUN pip install pillow

# RUN apk add --no-cache jpeg-dev zlib-dev git nano
# RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
#     && pip install Pillow

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN pip install django-user-agents==0.4.0

COPY . /app
EXPOSE 8000

RUN python3 manage.py makemigrations && python manage.py migrate
RUN cp /app/wvapi/settings/dock.prod.py /app/wvapi/settings/local.py 


CMD  gunicorn wvapi.wsgi:application --workers=2 --timeout=120  -b 0.0.0.0:8000