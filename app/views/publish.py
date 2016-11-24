#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/25


from json import dumps

from flask import Blueprint, render_template, request
from flask import flash
from flask_login import login_required

from app.utils.salt import SaltApi
from ..forms.publish import push
from ..models import Group, Host

publish = Blueprint('publish',
                    __name__,
                    url_prefix='/dashboard/publish')


@publish.route('/', methods=['GET', 'POST'])
@login_required
def index():
    salt = SaltApi()
    form = push()
    grouplist = Group.query.all()  # 获取所有组
    hostlist = Host.query.all()  # 获取所有主机
    if form.validate_on_submit():
        group = request.values.get('group')  # 页面选中的组名
        clientlist = Host.query.filter_by(host_group=group).all()  # 通过组来查询主机
        host = request.values.getlist('host')  # 主机名
        version = request.values.get('version')
        path = " ".join(form.path.data.split())  # 页面中的文件路径
        username = request.values.get('username')
        password = request.values.get('password')

        if clientlist and len(host) == 0:
            # 通过组来获取所有主机
            hosttgt = ",".join([i.host_name for i in clientlist])
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
                           hostlist=hostlist,
                           form=form,
                           title="项目发布"
                           )
