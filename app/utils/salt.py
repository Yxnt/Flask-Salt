#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/25

import json
import os
from collections import OrderedDict

from requests import session, get

from app import config
from .logger import log

config = config[os.environ.get('FLASK_ENV') or 'dev']


class SaltApi():
    headers = {'Accept': 'application/json'}
    url = config.SALT_URL
    user = config.SALT_USER
    passwd = config.SALT_PASS
    result = OrderedDict()

    @staticmethod
    def post(url, data, headers):
        response = session().post(url, data=data, headers=headers)
        return response

    def datainfo(self, tgtlist, fun, arg):
        datainfo = {
            'client': 'local',
            'tgt': tgtlist,
            'expr_form': 'list',
            'fun': fun,
            'arg': arg

        }
        return datainfo

    @property
    def login(self):
        login_url = "%s/login" % self.url
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
        # self.result['result'].append()
        log.info(self.result)
        return self.result

    def command(self, cmd):
        pass

    def testping(self, tgtlist, fun='test.ping', arg=None):
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
        log.info(self.result)
        return self.result

    def getjid(self, tgtlist):
        url = "%s/jobs/%s" % (self.url, self.testping(tgtlist))

        print(get(url, headers=self.login, timeout=3000).text)


        # result = json.loads(response.text)['info'][0]['Result']
        # print(result)

    def get_minion(self):
        pass
