#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/18


import os

from . import Config

try:
    from app.utils.logger import handler
except:
    os.mkdir('log')
    from app.utils.logger import handler


class Development(Config):
    '''本地调试配置'''
    DEBUG = True

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

    def init_app(app):
        app.logger.addHandler(handler)
