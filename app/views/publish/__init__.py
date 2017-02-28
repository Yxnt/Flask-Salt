#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Blueprint

publish = Blueprint('publish',__name__)

from . import views