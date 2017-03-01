#!/usr/bin/env python
#-*- coding:utf-8 -*-
from flask import render_template

from . import publish

@publish.route('/git')
def git():
    return render_template('publish/git.html')

@publish.route('/status')
def status():
    pass