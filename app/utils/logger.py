#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/11/1

import logging
import datetime

from logging.handlers import RotatingFileHandler


nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
LOG_PATH_FILE = 'log/{time}.log'.format(time=nowdate)
LOG_MODE = 'a'
LOG_MAX_SIZE = 50 * 1024 * 1024
LOG_MAX_FILES = 4
LOG_LEVEL = logging.DEBUG

LOG_FORMAT = "%(asctime)s %(levelname)-10s[%(filename)s:%(lineno)d(%(funcName)s)] %(message)s"

handler = RotatingFileHandler(
    filename=LOG_PATH_FILE,
    mode=LOG_MODE,
    maxBytes=LOG_MAX_SIZE,
    backupCount=LOG_MAX_FILES,
    encoding='utf-8'
)

# formatter = logging.Formatter(LOG_FORMAT)
# handler.setFormatter(formatter)
# handler.setLevel(LOG_LEVEL)







