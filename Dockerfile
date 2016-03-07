FROM python:latest

RUN mkdir -p /app
WORKDIR /app
CMD gunicorn -w 2 -k sync -b "0.0.0.0:80" project.wsgi:application

RUN pip install --upgrade pip
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY requirements-dev.txt /app
RUN pip install -r requirements-dev.txt

COPY . /app

# Collect static files
RUN SECRET_KEY='4&o4wx)z4l3=zk85p(h)q08^2fvfjg^fpkmhjy=i%iu^azboig' \
    RAVEN_DSN='' \
    TVDB_API_KEY='' \
    ./manage.py collectstatic --noinput
