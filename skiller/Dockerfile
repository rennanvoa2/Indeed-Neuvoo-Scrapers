FROM python:3

COPY . /opt/app
WORKDIR /opt/app/cfg

RUN pip install -r requirements.txt
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


WORKDIR /opt/app/

#install crontab and nano
RUN apt-get update -y
RUN apt-get install cron -y
RUN apt-get install nano -y


#copy the crontab file to crontab
RUN crontab crontab

RUN service cron start

WORKDIR /opt/app/src/collector
