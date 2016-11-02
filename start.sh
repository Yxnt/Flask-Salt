#!/bin/sh
FLASK_ENV='pro'
/data/web/salt/venv/bin/gunicorn manage:app -c /data/web/salt/gunicorn.conf
