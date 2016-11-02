#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/18


from . import Config


class development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://salt:123456@localhost/salt?charset=utf8'
    SALT_URL = 'http://10.1.5.253:8080'
    SALT_USER = 'salt'
    SALT_PASS = '1234'


