#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/14

from flask import Blueprint, render_template

cdn = Blueprint('cdn',
                __name__,
                url_prefix='/dashboard/cdn')

@cdn.route('/')
def downloadlog():
    return render_template('cdn/index.html')