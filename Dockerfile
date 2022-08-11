FROM python:3.8-slim-buster

WORKDIR /django

COPY . .

RUN ["pip", "install", "-r", "requirements.txt"]

WORKDIR /django/url_shortener

RUN ["./manage.py", "migrate"]

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
