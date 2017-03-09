#!/bin/sh
export FLASK_ENV='pro'
export SECRET_KEY='this is flask wtf secret_key'
/data/web/salt/venv/bin/gunicorn manage:app -c /data/web/salt/gunicorn.conf
