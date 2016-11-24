#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/18

from . import Config


class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://salt:123456@localhost/salt?charset=utf8'
    SALT_URL = 'http://172.31.32.5:1122'
    SALT_USER = 'salt'
    SALT_PASS = 'salt'
