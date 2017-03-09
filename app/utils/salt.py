#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/25


import json
import os
from requests import session
import urllib.parse as urljoin

from app import config
from app.utils.cache import RedisCli

# 读取配置文件
config = config[os.environ.get('FLASK_ENV') or 'dev']



class SaltApi(object):
    '''调用saltAPI来完成操作'''
    headers = {'Accept': 'application/json'}
    url = config.SALT_URL
    user = config.SALT_USER
    passwd = config.SALT_PASS
    eauth = config.SALT_EAUTH
    redis_key = 'salt:user:{user}:login'.format(user=user)
    redis = RedisCli(
        ip=config.REDIS_IP,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
        password=config.REDIS_PASS
    )

    def __init__(self):
        self.auth = {}

    def req(self, path, info):
        """
        POST方式执行salt任务
        :param path: salt api uri
        :param info: json info
        :return: saltstack json info
        """
        urlpath = urljoin.urljoin(self.url, path)
        headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }
        if self.r.get(self.redis_key):
            token = json.loads(self.r.get(self.redis_key).decode('utf-8'))
            headers['X-Auth-Token'] = token['X-Auth-Token']

        s = session()
        info = json.dumps(info)
        ret = s.post(urlpath, info, headers=headers)
        return ret

    def req_get(self, path):
        """
        GET方式获取salt信息
        :param path: salt api uri
        :return: saltstack json info
        """
        urlpath = urljoin.urljoin(self.url, path)
        headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }
        token = json.loads(self.r.get(self.redis_key).decode('utf-8'))

        headers['X-Auth-Token'] = token['X-Auth-Token']

        s = session()
        ret = s.get(urlpath, headers=headers)
        return ret



    def login(self):
        redis_key = 'salt:user:{user}:login'.format(user=self.user)
        if self.r.get(redis_key):
            self.auth = self.r.get(redis_key)
            return self.auth
        else:
            login_info = {
                'username': self.user,
                'password': self.passwd,
                'eauth': self.eauth
            }
            ret_info = self.req('/login', login_info).json()['return'][0]

            start_time = ret_info['start']
            end_time = ret_info['expire']
            expire_time = int(end_time - start_time)
            token = ret_info['token']
            self.auth['X-Auth-Token'] = token
            self.r.set(redis_key, json.dumps(self.auth), expire_time)
            return self.auth

    @property
    def stats(self):
        ret_info = self.req_get('/stats').json()
        return ret_info

    @property
    def jobs(self):
        ret_info = self.req_get('/jobs').json()
        return ret_info

    @property
    def minion(self):
        ret_info = self.req_get('/minions').json()
        return ret_info

    @property
    def keys(self):
        ret_info = self.req_get('/keys').json()
        return ret_info

    def run(self, fun, arg, tgt):
        """
        saltstack runner 
        :param fun: 要执行的modules
        :param arg: 提交的参数
        :param tgt: 操作的host节点
        :return: 操作结果
        """
        data_info = [{
            "client": "local",
            "tgt":tgt,
            "fun": fun
        }]

        if arg:
            data_info[0]['arg'] = arg

        ret_info = self.req('', data_info).json()
        return ret_info