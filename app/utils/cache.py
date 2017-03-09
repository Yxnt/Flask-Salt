#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/11/17

import redis


class RedisCli(object):
    """自定义操作redis类"""
    def __init__(self, ip, port, db, password, **kwargs):
        self.ip = ip
        self.port = port
        self.db = db
        self.password = password

    def __connect(self):
        pool = redis.ConnectionPool(
            host=self.ip,
            port=self.port,
            db=self.db,
            password=self.password
        )
        return redis.Redis(connection_pool=pool)

    def __r(self):
        return self.__connect()

    def get(self, key):
        return self.__r().get(key)

    def set(self, key, value, time):
        if self.get(key):
            return self.get(key)
        else:
            return self.__r().set(key, value, ex=time)
