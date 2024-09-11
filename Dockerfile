
from ubuntu:20.04

RUN apt update --fix-missing

RUN apt install -y python3-pip  git 
RUN pip install pillow

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . /app
EXPOSE 8000

RUN cp /app/wvapi/settings/dock.prod.py /app/wvapi/settings/local.py 


CMD (python manage.py migrate || true) && (python manage.py collectstatic --noinput || true) &&  gunicorn wvapi.wsgi:application --workers=2 --timeout=120  -b 0.0.0.0:8000