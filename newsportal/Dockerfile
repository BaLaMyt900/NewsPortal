FROM python:alpine
LABEL authors="BaLaMyt900"

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
#RUN apk add --no-cache openrc && apk add redis

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN apk add --update redis && \
    rm -rf /var/cache/apk/* && \
    mkdir /data/redis && \
    chown -R redis:redis /data/redis && \
    echo -e "include /etc/redis-local.conf\n" >> /etc/redis.conf \
ADD root /
VOLUME ["/data/redis"]
EXPOSE 6379