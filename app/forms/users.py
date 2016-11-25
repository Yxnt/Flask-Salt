#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/18

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    '''登陆FORM组件'''
    username = StringField("用户名", validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    rember = BooleanField()
