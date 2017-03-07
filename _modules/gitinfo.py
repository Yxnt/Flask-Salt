#!/usr/bin/env python
# -*- coding:utf-8 -*-
from git import Repo
from os import path, listdir
from salt import client
from json import dumps
import redis

__outputter__ = {__name__: 'json'}

result = []
try:
    cli = client.LocalClient()
except Exception:
    pass

def _loop(dire, ret):
    """遍历目录
    :param dire: 指定目录名称
    :param ret: 结果保存值
    :return: None
    """
    for i in listdir(dire):
        file_name = path.join(dire, i)
        if path.isdir(file_name):
            _loop(file_name,ret)
        else:
            file_name = '/'.join(file_name.split('/')[6:])
            ret.append(file_name)

def get_path(project_name):
    project_path = path.join('/srv/salt/file/Release', project_name)
    return project_path


def get_branches(project_name):
    result = {}
    repo = Repo(get_path(project_name))
    refs = repo.remotes.origin.refs
    n = 0
    for i in refs:
        result[n] = i.name
        n += 1
    return result


def get_master_all_hex(project_name):
    hexsha_history = list()
    repo = Repo(get_path(project_name))
    hc = repo.iter_commits('origin/master')
    repo.remotes.origin.fetch()
    for i in hc:
        hexsha_history.append(i.hexsha.encode('utf-8'))
    return list(set(hexsha_history))


def get_master_cur_hex(project_name):
    repo = Repo(get_path(project_name))
    hc = repo.commit('master')
    return hc.hexsha.encode('utf-8')


def reset(project_name, newhex, host):
    repo = Repo(get_path(project_name))
    result = repo.head.reset(newhex, index=True, working_tree=True).name

    pool = redis.ConnectionPool(
        host='',
        port='',
        db=None,
        password=''
    )
    r = redis.Redis(connection_pool=pool)
    key = 'salt:publish:salt:save_res'
    value = []
    _loop(get_path(project_name),value)
    r.set(key,dumps(value))
    r.expire(key, 180)

    host = ','.join(host)
    if result == 'HEAD':
        cli.cmd(
            host,
            'cp.get_dir',
            ['salt://file/Release/%s' % project_name, 'D:/ops', 'gzip=5'],
            expr_form='list')
        ret = cli.cmd(
            host,
            'diff.diff',
            ['D:/ops/%s' % project_name, 'E:/Release/%s' % project_name],
            expr_form='list')
        return ret
