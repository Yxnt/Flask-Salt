#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  flask import Blueprint

user = Blueprint('users', __name__,
                 url_prefix='/user',
                 )

from . import views