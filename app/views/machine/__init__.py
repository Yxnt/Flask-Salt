#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  flask import Blueprint

machine = Blueprint('machine', __name__)

from . import views