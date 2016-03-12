# TV Tracker

[![Build Status](https://travis-ci.org/kvikshaug/tv-tracker.svg?branch=master)](https://travis-ci.org/kvikshaug/tv-tracker)
[![Requirements Status](https://requires.io/github/kvikshaug/tv-tracker/requirements.svg?branch=master)](https://requires.io/github/kvikshaug/tv-tracker/requirements/?branch=master)

Keep track of the TV series you're watching, what episodes you've seen and when the next one is coming out.

## Development

### Environment

* `SECRET_KEY`: [Django's SECRET_KEY setting](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY)
* `RAVEN_DSN`: [Raven DSN](https://docs.getsentry.com/hosted/clients/python/integrations/django/)
* `TVDB_API_KEY`: [TheTVDB API key](http://thetvdb.com/?tab=apiregister)
* `RECAPTCHA_PUBLIC_KEY`: [Recaptcha public key](https://www.google.com/recaptcha/intro/index.html)
* `RECAPTCHA_PRIVATE_KEY`: [Recaptcha private key](https://www.google.com/recaptcha/intro/index.html)

### Start development server

```
docker-compose up
```

### Compile statics

```
docker-compose run --rm builder sass --scss --update scss:css
docker-compose run --rm app ./manage.py collectstatic --noinput
```

### QA

```
docker-compose run --rm app flake8 --config=flake8.cfg .
docker-compose run --rm app ./manage.py test
```
