# start from base image of python3.7 on alpine linux
#FROM python:3.7-alpine
FROM ubuntu:18.04

# set environment variables for container
#ENV BACKEND_DIR=/opt/

# install required system components (python3, pip3, django, nginx, uswgi)
RUN set -ex; \
    echo "Updating Ubuntu" \
        && apt-get update; \
    echo "Installing Python3 and Pip" \
        && apt install -y python3 \
        && apt install -y python3-pip; \
        #&& pip install -U pip \
    echo "Installing django and required packages" \
        #USE FOLLOWING LINE WHEN TESTING WITH ACTUAL REPO
        #&& pip3 install -r static/requirements.txt;
        && pip3 install django; \
    echo "Installing nginx and uswgi" \
        && apt install nginx uwsgi uwsgi-plugin-python3 -y;

# leaving installations as separate layer, since we will need to 
# rebuild often during integration testing  to change API targets within 
# the api.py files and want the component installations to be cached so
# we won't have to wait as long

# copy backend files to container
COPY mysite /home/mysite

# change to directory with manage.py and requirements.txt
WORKDIR /home

# set up ngnix as server for django
RUN set -ex; \
    echo "Make directories for static (non python) files and media files" \
        && mkdir -p /home/static /home/media \
        && chown www-data.www-data /home/media; \
    echo "Copy all static files to STATIC_ROOT (/home/static/)" \
        && python3 mysite/manage.py collectstatic; \
    echo "Move uwsgi and nginx config files to proper directories" \
        && mkdir -p /etc/uwsgi/apps-enabled \
        && mkdir -p /etc/nginx/site-enabled \
        && mv mysite/django.ini /etc/uwsgi/apps-enabled/django.ini \
        && mv mysite/django /etc/nginx/site-enabled/django; 
#    echo "Restart uWSGI and Nginx" \
#        && service uwsgi restart \
#        && service nginx restart;
#CMD ["python3", "manage.py", "runserver", "8888"]
CMD ["sh"]
