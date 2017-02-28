#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/13


from flask import render_template, session
from flask import redirect, url_for
from flask_login import logout_user, login_required

from app.forms.users import LoginForm
from . import user


@user.route('/login')
def login():
    return render_template('user/views.html',
                           title="登陆",
                           login_form=LoginForm())


@user.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('user.login'))
