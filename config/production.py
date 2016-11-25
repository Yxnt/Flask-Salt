#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/18

from . import Config


class Production(Config):
    '''线上配置文件'''
    DEBUG = False

    # DB Config
    DBUSER = None
    DBPASS = None
    DBHOST = None
    DNNAME = None

    # DB String
    SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}?charset=utf8'.format(
        dbuser=DBUSER,
        dbpass=DBPASS,
        dbhost=DBHOST,
        dbname=DBHOST
    ))

    # SaltAPI
    SALT_URL = ''
    SALT_USER = ''
    SALT_PASS = ''