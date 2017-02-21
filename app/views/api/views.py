#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import flash, redirect, request
from flask import url_for
from flask_login import login_user

from . import api
from app.models import User


@api.route('/auth', methods=['POST'])
def auth():
    # 查找用户名
    remember = 'False'
    if request.form['rember'] :
        remember = request.form['rember']
    user_name = User.query.filter_by(user_name=request.form['username']).first()
    try:
        # 将用户输入的密码进行加密来验证
        user_pass = user_name.verify_password(request.form['password'])
    except AttributeError:
        flash("账号或密码错误", category='usererror')
        return redirect(request.referrer)
    if user_name is not None and user_pass:
        login_user(user_name,remember=True)
        return redirect(url_for('dashboard.index'))

        # 登陆成功后跳转到之前的页面或者跳转到首页
        # try:
        #     return redirect(url_for('dashboard.index'))
        # except NameError:
        #     return redirect(url_for('dashboard.index'))
    else:
        flash("账号或密码错误", category='error')
        return redirect(request.referrer)
