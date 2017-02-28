#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/11

from flask import Flask
from flask_assets import Environment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import development, production
from .utils import assets
from .utils.assets import bundles

login_manager = LoginManager()
csrf = CSRFProtect()
db = SQLAlchemy()

config = {
    'dev': development.Development,
    'pro': production.Production,
}

app = Flask(__name__)


def create_app(config_name):
    '''初始化 应用'''
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.session_protection = "strong"
    login_manager.login_view = 'user.login'  # 未认证用户跳转

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    assets = Environment(app)
    assets.register(bundles)

    from app.views import user
    from app.views import dashboard
    from app.views import api
    from app.views import machine
    from app.views import publish

    app.register_blueprint(user)
    app.register_blueprint(dashboard)
    app.register_blueprint(api)
    app.register_blueprint(machine)
    app.register_blueprint(publish)

    return app
