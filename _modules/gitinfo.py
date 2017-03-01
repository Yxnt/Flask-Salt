#!/usr/bin/env python
#-*- coding:utf-8 -*-
from git import Repo
from os import path
from salt import client
__outputter__ = { __name__: 'json'}

def get_path(project_name):
    project_path = path.join('/srv/salt/file/Release',project_name)
    return project_path

def get_branches(project_name):
    result = {}
    repo = Repo(get_path(project_name))
    refs = repo.remotes.origin.refs
    n = 0
    for i in refs:
        result[n] = i.name
        n+=1
    return result

def get_master_all_hex(project_name):
    result = {}
    hexsha_history = list()
    repo = Repo(get_path(project_name))
    hc = repo.iter_commits('master')
    repo.remotes.origin.fetch()
    remote = repo.remotes.origin.refs.master.log()
    if remote:
        hexsha_history.append(remote[-1].newhexsha.encode('utf-8'))
    for i in hc:
        hexsha_history.append(i.hexsha.encode('utf-8'))
    return hexsha_history
    
def get_master_cur_hex(project_name):
    repo = Repo(get_path(project_name))
    hc = repo.commit('master')
    return hc.hexsha.encode('utf-8')


def reset(project_name, newhex, host):
    repo = Repo(get_path(project_name))
    result = repo.head.reset(newhex,index=True,working_tree=True).name
    if result == 'HEAD':
        cli = client.LocalClient()
        host = ",".join(host)
        ret = cli.cmd(host,'cp.get_dir',['salt://file/Release/%s' % project_name,'E:/Release','gzip=5'],expr_form='list')
        return ret

