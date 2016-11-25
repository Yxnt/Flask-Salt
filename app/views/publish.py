#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/25


from json import dumps

from flask import Blueprint, render_template, request, flash
from flask_login import login_required

from app.utils.salt import SaltApi
from ..forms.publish import Push
from ..models import Group
from ..models import Host

publish = Blueprint('publish',
                    __name__,
                    url_prefix='/dashboard/publish')


@publish.route('/', methods=['GET', 'POST'])
@login_required
def index():
    '''发布页面操作'''
    salt = SaltApi()
    form = Push()
    grouplist = Group.query.all()  # 获取所有组
    hostalllist = Host.query.all()  # 获取所有主机
    if form.validate_on_submit():
        group = request.values.get('group')  # 页面选中的组名
        clientlist = Group.query.filter_by(group_name=group).all()

        for i in clientlist:
            global hostlist
            hostlist = [l.host_name for l in i.host_name.all()]

        host = request.values.getlist('host')  # 主机名
        version = request.values.get('version')
        path = " ".join(form.path.data.split())  # 页面中的文件路径
        username = request.values.get('username')
        password = request.values.get('password')

        if clientlist and len(host) == 0:
            # 通过组来获取所有主机
            hosttgt = ",".join(hostlist)
            result = salt.svnupdate(
                tgtlist=hosttgt,
                username=username,
                password=password,
                path=path,
                version=version
            )
            result = dumps(result, indent=2)
            flash(result, category="info")
        elif clientlist and host:
            # 主机和组不能同时选择
            flash("主机和组不能同时选择", category="warning")
        elif host:
            # 只操作主机
            hosttgt = ",".join(host)
            result = dumps(salt.svnupdate(
                tgtlist=hosttgt,
                username=username,
                password=password,
                path=path,
                version=version
            ), indent=2)
            flash(result, category='info')
        else:
            flash("请选择组或者主机", category="warning")

    return render_template('publish/index.html',
                           grouplist=grouplist,
                           hostlist=hostalllist,
                           form=form,
                           title="项目发布"
                           )
