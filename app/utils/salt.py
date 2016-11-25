#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/25


import json
import os
from collections import OrderedDict

from requests import session, get

from app import config

# 读取配置文件
config = config[os.environ.get('FLASK_ENV') or 'dev']


class SaltApi(object):
    '''调用saltAPI来完成操作'''
    headers = {'Accept': 'application/json'}
    url = config.SALT_URL
    user = config.SALT_USER
    passwd = config.SALT_PASS
    result = OrderedDict()  # 结果返回为一个有序字典

    @staticmethod
    def post(url, data, headers):
        response = session().post(url, data=data, headers=headers)
        return response

    @staticmethod
    def datainfo(tgtlist, fun, arg):
        datainfo = {
            'client': 'local',
            'tgt': tgtlist,
            'expr_form': 'list',  # 操作多个主机
            'fun': fun,
            'arg': arg
        }
        return datainfo

    @property
    def login(self):
        '''登陆saltapi'''
        login_url = "{domain}/login".format(domain=self.url)
        logininfo = {
            'username': self.user,
            'password': self.passwd,
            'eauth': 'pam'
        }
        response = self.post(login_url, data=logininfo, headers=self.headers)
        token = json.loads(response.text)['return'][0]['token']
        data = {
            'X-Auth-Token': token
        }
        return data

    def svnupdate(self, tgtlist, version, path, username, password, fun='cmd.run'):
        '''svn更新函数，'''
        cmd = 'svn update -r {version} ' \
              '--username {username} ' \
              '--password {password} ' \
              '--accept tc {path}'.format(
            version=version,
            username=username,
            password=password,
            path=path
        )
        response = self.post(
            url=self.url,
            headers=self.login,
            data=self.datainfo(
                tgtlist=tgtlist,
                fun=fun,
                arg=cmd
            )
        )
        self.result['operator'] = 'svn update'
        self.result['path'] = path
        self.result['version'] = version
        self.result['username'] = username
        self.result['result'] = json.loads(response.text)['return']
        print(response.text)
        return self.result

    def command(self, cmd):
        pass

    def testping(self, tgtlist, fun='test.ping', arg=None):
        '''判断主机是否存活'''
        response = self.post(
            url=self.url,
            data=self.datainfo(
                tgtlist,
                fun,
                arg
            ), headers=self.login)

        self.result['operator'] = fun
        self.result['arg'] = arg
        self.result['result'] = json.loads(response.text)['return'][0]

        return self.result

    # def getjid(self, tgtlist):
    #     url = "%s/jobs/%s".format(self.url, self.testping(tgtlist))
    #
    #     print(get(url, headers=self.login).text)
    #
    # def get_minion(self, minion):
    #     if minion or minion != '*':
    #         url = '%s/minion/%s'
