#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  flask import Blueprint

dashboard = Blueprint('dashboard',
                      __name__)
from . import views