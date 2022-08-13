FROM python:3.8-slim-buster

WORKDIR /django

COPY requirements.txt requirements.txt

RUN ["pip", "install", "-r", "requirements.txt"]

# ? If you wanna start django app without postgres on docker, 
# ? uncomment next 3 lines, Then change settings.py, DATABASE part
# ? Then run: "$ docker build ."
# COPY . .
# WORKDIR /django/url_shortener
# RUN ["./manage.py", "migrate"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
