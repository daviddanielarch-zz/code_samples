FROM python:3.5

ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT python manage.py runserver 0.0.0.0:8000
