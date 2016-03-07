import multiprocessing

# http://docs.gunicorn.org/en/latest/configure.html
# http://docs.gunicorn.org/en/latest/settings.html

bind = ['0.0.0.0:8000']
worker_class = 'sync'
forwarded_allow_ips = '*'
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 60
