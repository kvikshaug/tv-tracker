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

## Features

- Add your shows and categorize them by **active**, **default** and **archived**
- Keep track of which episode you last watched
- See which unseen episodes are available
- See when the next episode is coming out
- Data synchronized each night from [thetvdb.com](http://thetvdb.com/)

## How to play

- Get an API key from [TheTVDB](http://thetvdb.com/wiki/index.php?title=Programmers_API)
- Configure `crontab` to run `manage.py sync_all_series` each night
- Set up your database, run all database migrations
- Set up a standard Django installation and webserver
- *(Optional)* set up Sentry for error logging
- [Should work now](https://www.google.com/search?tbm=isch&q=ponies)

## Screenshots

If the words above make no sense

### The dashboard shows you what's up

![No soup for eyehandicappeds](https://kvikshaug.github.io/tv-tracker/index.jpg "Index")

### Search for and add new shows

![No soup for eyehandicappeds](https://kvikshaug.github.io/tv-tracker/search.jpg "Search")

### Show details

![No soup for eyehandicappeds](https://kvikshaug.github.io/tv-tracker/show.jpg "Show")
