#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/17

from flask import Blueprint, url_for, render_template
from flask_login import login_required

dashboard = Blueprint('dashboard',
                      __name__,
                      url_prefix='/dashboard')


@dashboard.route('/')
@dashboard.route('/index')

def index():
    return render_template('dashboard/index.html')