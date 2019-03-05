FROM python:3.6

ENV PYTHONUNBUFFERED 1
# set working directory
RUN mkdir -p /usr/apps/my-blog/back-end
WORKDIR /usr/apps/my-blog/back-end
# install and cache app dependencies
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
# add app
ADD . .
