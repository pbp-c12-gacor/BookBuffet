FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=BookBuffet.settings \
    PORT=8000 \
    WEB_CONCURRENCY=2 \
    DATABASE_URL=postgres://bookbuffet_user:0qPJN5DudGY4EHT2LiZq2h9m66bcTVi8@dpg-clktrosjtl8s73f2mo80-a.singapore-postgres.render.com/bookbuffet

# Install system packages required Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
&& rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy project code
COPY . .

RUN python manage.py collectstatic --noinput --clear

# Run as non-root user
RUN chown -R django:django /app
USER django

# Run application
# CMD gunicorn BookBuffet.wsgi:application