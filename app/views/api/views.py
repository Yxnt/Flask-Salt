#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import flash, redirect, request, session, jsonify, abort
from flask import url_for
from flask_login import login_user
from functools import wraps
import re

from . import api
from app.models import User
from app.utils.salt import SaltApi

s = SaltApi()


@api.route('/auth', methods=['POST'])
def auth():
    # 查找用户名
    user_name = User.query.filter_by(user_name=request.form['username']).first()
    try:
        # 将用户输入的密码进行加密来验证
        user_pass = user_name.verify_password(request.form['password'])
    except AttributeError:
        flash("账号或密码错误", category='usererror')
        return redirect(request.referrer)
    if user_name is not None and user_pass:
        if 'rember' in request.form:
            login_user(user_name, remember=request.form['rember'])
        else:
            login_user(user_name)
        session['username'] = request.form['username']
        if not s.redis.get(s.redis_key):
            s.login()
        return redirect(url_for('dashboard.index'))
    else:
        flash("账号或密码错误", category='error')
        return redirect(request.referrer)


def check(fun):
    @wraps(fun)
    def user(operator=None):
        if 'username' in session and operator:
            return jsonify(fun(operator))
        elif 'username' in session:
            return jsonify(fun())
        else:
            abort(401)

    return user


@api.route('/salt/stats')
@check
def stats():
    for k, v in s.stats.items():
        m = re.match(r"CherryPy HTTPServer.*", k)
        if m:
            return s.stats[m.group(0)]


@api.route('/salt/jobs')
@check
def job():
    return s.jobs


@api.route('/salt/minions')
@check
def minion():
    return s.minion


@api.route('/salt/keys')
@check
def keys():
    return s.keys


@api.route('/salt/publish/git/<operator>', methods=['GET', 'POST'])
@check
def git(operator):
    post_info = request.get_json()
    if len(post_info) != 4:
        data = s.run(fun='gitinfo.{fun}'.format(fun=operator), arg=post_info, tgt='master')
    else:
        data = s.run(fun='gitinfo.{fun}'.format(fun=operator), arg=post_info[1:], tgt=post_info[0])
    return data
