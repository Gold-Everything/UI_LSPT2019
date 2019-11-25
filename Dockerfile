# start from base image of python3.7 on alpine linux
FROM python:3.7-alpine

# set environment variables for container
#ENV BACKEND_DIR=/opt/

# copy backend files to container
COPY UI /opt/

# change to directoru with manage.py and requirements.txt
WORKDIR /opt/UI

RUN set -ex; \
    echo "Updating Alpine packages:" \
        && apk --no-cache upgrade; \
    ehco "Updating pip, installing all required packages" \
        && pip install -U pip \
        && pip install -r static/requirements.txt;
        #&& pip install django;

CMD ["python3", " manage.py", "runserver", "8888"]

