FROM python:alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
LABEL authors="BaLaMyt900"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/