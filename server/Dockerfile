FROM tiangolo/uwsgi-nginx:python3.6

EXPOSE 5000

# set up environment variables
ENV UWSGI_INI /encabulary.uwsgi.ini

# copy application
COPY server /app/server
COPY config.py /app
COPY initdb.py /app
COPY runserver.py /app

# copy configs
COPY encabulary.nginx.conf /etc/nginx/conf.d/
COPY encabulary.uwsgi.ini /
COPY requirements.txt /

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /requirements.txt

WORKDIR /app
