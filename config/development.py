#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/18
from datetime import timedelta

from . import Config


class Development(Config):
    '''本地调试配置'''
    DEBUG = True
    # login cookie expirse
    REMEMBER_COOKIE_DURATION = timedelta(hours=2)
    # DB Config
    DBUSER = ""
    DBPASS = ""
    DBHOST = ""
    DNNAME = ""

    # DB String
    SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}?charset=utf8'.format(
        dbuser=DBUSER,
        dbpass=DBPASS,
        dbhost=DBHOST,
        dbname=DNNAME
    ))

    # SaltAPI
    SALT_URL = ''
    SALT_USER = ''
    SALT_PASS = ''
    SALT_EAUTH = ''

    # redis
    REDIS_IP = ''
    REDIS_PORT = ''
    REDIS_DB = ''
    REDIS_PASS = ''

    def init_app(app):
        pass