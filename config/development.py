#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/18

from . import Config


class Development(Config):
    '''本地调试配置'''
    DEBUG = True
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
    SALT_URL = ''
    SALT_USER = ''
    SALT_PASS = ''

    def init_app(app):
        pass