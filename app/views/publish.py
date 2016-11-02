#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/25


from flask import Blueprint, render_template, request
from flask import flash

from app.utils.salt import SaltApi
from ..forms.publish import push
from ..models import Group, Host

from json import dumps


publish = Blueprint('publish',
                    __name__,
                    url_prefix='/dashboard/publish')


@publish.route('/', methods=['GET', 'POST'])
# @login_required
def index():
    salt = SaltApi()
    hosttgt = []
    form = push()
    grouplist = Group.query.all()
    hostlist = Host.query.all()
    if form.validate_on_submit():
        group = request.values.get('group')
        clientlist = Host.query.filter_by(host_group=group).all()
        host = request.values.getlist('host')

        version = request.values.get('version')
        project = request.values.get('project')
        username = request.values.get('username')
        password = request.values.get('password')

        if group and len(host) == 0:
            for i in clientlist:
                hosttgt.append(i.host_name)

            tgt = ",".join(hosttgt)

            result = salt.svnupdate(
                tgtlist=tgt,
                username=username,
                password=password,
                path=project,
                version=version
            )
            result = dumps(result, indent=2)
            flash(result,category="info")
        elif host:
            print(2)
        else:
            flash("请选择组或者主机",category="warning")

    return render_template('publish/index.html',
                           grouplist=grouplist,
                           hostlist=hostlist,
                           form=form,
                           title="项目发布"
                           )
