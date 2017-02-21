#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  flask import Blueprint

dashboard = Blueprint('dashboard',
                      __name__,
                      url_prefix='/dashboard')
from . import views