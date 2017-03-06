#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Created by Yxn on 2017/2/27.

from flask import render_template

from . import machine


@machine.route("/host")
def host():
    return render_template('asset/host.html')
