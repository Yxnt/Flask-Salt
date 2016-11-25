#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/13


from flask import Blueprint, render_template, request, flash
from flask import redirect, url_for
from flask_login import login_user, logout_user, login_required

from ..forms import users
from ..models import User

user = Blueprint('users', __name__,
                 url_prefix='/user',
                 )


def login_form():
    return users.LoginForm()


global nextpage


@user.route('/login')
def login():
    nextpage = request.args.get('next')
    return render_template('user/login.html',
                           title="登陆",
                           login_form=login_form())


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@user.route('/auth', methods=['POST'])
def auth():
    if login_form().validate_on_submit():
        # 查找用户名
        user_name = User.query.filter_by(user_name=request.form['username']).first()
        try:
            # 将用户输入的密码进行加密来验证
            user_pass = user_name.verify_password(login_form().password.data)
        except AttributeError:
            flash("账号或密码错误", category='usererror')
            return redirect(request.referrer)
        if user_name is not None and user_pass:
            login_user(user_name, login_form().rember.data)
            # 登陆成功后跳转到之前的页面或者跳转到首页
            try:
                return redirect(nextpage or url_for('dashboard.index'))
            except NameError:
                return redirect(url_for('dashboard.index'))
    flash("账号或密码错误", category='error')
    return redirect(request.referrer)
