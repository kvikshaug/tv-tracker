#!/bin/bash
source /mnt/secrets/secrets.env && gunicorn -c gunicorn.py project.wsgi:application
