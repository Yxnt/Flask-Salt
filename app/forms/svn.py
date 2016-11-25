#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/17

from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, URL


class Svn(FlaskForm):
    '''SVN权限开通'''
    svnlist = TextAreaField(validators=[DataRequired(), URL()])
