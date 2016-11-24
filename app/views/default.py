#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/11/16

from flask import Blueprint
from flask import redirect
from flask import url_for
from flask_login import login_required

default = Blueprint('default',__name__)

@default.route('/')
@login_required
def index():
    return redirect(url_for('dashboard.index'))




