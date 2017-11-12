#!/usr/bin/env bash

rsync -rhv --exclude-from .syncerignore ./ /usr/share/nginx/www/encabulary
rsync -rhv encabulary.supervisor.conf /etc/supervisor/conf.d/
rsync -rhv encabulary.uwsgi.ini /etc/uwsgi/
rsync -rhv encabulary.nginx.conf /etc/nginx/sites-available/
ln -sf /etc/nginx/sites-available/encabulary.nginx.conf /etc/nginx/sites-enabled

chown -R www-data /usr/share/nginx/www/encabulary

cd /usr/share/nginx/www/encabulary
python3 -m virtualenv env
env/bin/pip install -r requirements.txt

sudo service nginx restart
sudo supervisorctl update
sudo supervisorctl restart encabulary