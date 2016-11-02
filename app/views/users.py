#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/13


from flask import Blueprint, render_template, request
from flask import flash
from flask import redirect
from flask import url_for

from ..forms import users
from ..models import User

user = Blueprint('users', __name__,
                 url_prefix='/user',
                 )


def login_form():
    return users.LoginForm()


@user.route('/login')
def login():
    return render_template('user/login.html',
                           title="登陆",
                           login_form=login_form())


@user.route('/auth', methods=['POST'])
def auth():
    if login_form().validate_on_submit():
        user_name = User.query.filter_by(user_name=request.form['username']).first()
        user_pass = user_name.verify_password(login_form().password.data)
        if user_name is not None and user_pass:
            return redirect(request.args.get('next') or url_for('dashboard.index'))
    flash()
