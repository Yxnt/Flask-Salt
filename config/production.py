#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/18

from . import Config
from datetime import timedelta

class Production(Config):
    '''线上配置文件'''
    DEBUG = False

    # login cookie expirse
    REMEMBER_COOKIE_DURATION = timedelta(hours=2)

    # db connection pooling
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_POOL_TIMEOUT = 120

    # DB Config
    DBUSER = None
    DBPASS = None
    DBHOST = None
    DBNAME = None

    # DB String
    SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}?charset=utf8'.format(
        dbuser=DBUSER,
        dbpass=DBPASS,
        dbhost=DBHOST,
        dbname=DBNAME
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