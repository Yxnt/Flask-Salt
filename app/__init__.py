#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/11

from flask import Flask
from flask_assets import Environment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

from config import development, production
from .utils import assets
from .utils.assets import bundles

login_manager = LoginManager()
csrf = CsrfProtect()
db = SQLAlchemy()

config = {
    'dev': development.development,
    'pro': production.Production,
}

app = Flask(__name__)


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.session_protection = "strong"
    login_manager.login_view = 'users.login' # 未认证用户跳转
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    assets = Environment(app)
    assets.register(bundles)
    from .views.cdn import cdn
    from .views.dashboard import dashboard
    from .views.svn import svn
    from .views.users import user
    from .views.publish import publish
    from .views.default import default

    # Blueprint
    app.register_blueprint(cdn)  # 日志下载页面
    app.register_blueprint(svn)  # svn管理
    app.register_blueprint(user)  # 注册用户页面
    app.register_blueprint(publish) # 发布
    app.register_blueprint(dashboard) # 后台页面
    app.register_blueprint(default) # 默认访问/

    # # Log
    # if not app.debug:
    #     app.logger.addHandler(handler)


    return app
