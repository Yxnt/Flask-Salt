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
    DBUSER = "salt"
    DBPASS = "MxvYjbOOYbUso"
    DBHOST = "10.19.80.15"
    DNNAME = "salt"

    # DB String
    SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}?charset=utf8'.format(
        dbuser=DBUSER,
        dbpass=DBPASS,
        dbhost=DBHOST,
        dbname=DNNAME
    ))

    # SaltAPI
    SALT_URL = 'http://10.19.80.12:8000'
    SALT_USER = 'salt'
    SALT_PASS = '123'
    SALT_EAUTH = 'pam'

    # redis
    REDIS_IP = '10.19.80.12'
    REDIS_PORT = '6379'
    REDIS_DB = '1'
    REDIS_PASS = 'Gmtj6KQjLmL1Q'

    def init_app(app):
        pass