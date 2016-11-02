#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/17


from flask import Blueprint, render_template
from flask_login import login_required
from ..forms.svn import Svn

svn = Blueprint('svn',
                __name__,
                url_prefix='/dashboard/svn')


@svn.route('/')
# @login_required
def index():
    form = Svn()

    return render_template('svn/index.html', form=form)
