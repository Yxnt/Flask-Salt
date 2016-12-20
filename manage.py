#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/11


import datetime
import os

from flask_script import Manager

from app import create_app, db
from app.models import User, Host, Group

app = create_app(os.environ.get('FLASK_ENV') or 'dev')
manager = Manager(app)


@manager.command
def createdb():
    "Create DataBase Tables"
    db.create_all()
    # for i in ['前台', '支付', '后台', '接口', '预发布', '其他']:
    #     site = Group(i)
    #     db.session.add(site)
    # db.session.commit()
    #
    # for i in ['JSSH2API0002', 'JSSH2API0003', 'JSSH2API0004', 'JSSH2API0005']:
    #     api = Host(i, '接口')
    #     db.session.add(api)
    #
    # for i in ['JSSH2WEB16002', 'JSSH2WEB16003', 'JSSH2WEB16004', 'JSSH2WEB16005', 'JSSH2WEB16006']:
    #     houtai = Host(i, '后台')
    #     db.session.add(houtai)
    #
    # for i in ['JSSH2WEB16007', 'JSSH2WEB16008', 'JSSH2WEB16009', 'JSSH2WEB16010', 'JSSH2WEB16011']:
    #     pay = Host(i, '支付')
    #     db.session.add(pay)
    #
    # for i in ['JSSH2WEB16012', 'JSSH2WEB16013', 'JSSH2WEB16014', 'JSSH2WEB16015', 'JSSH2WEB16016', 'JSSH2WEB16017']:
    #     host = Host(i, '前台')
    #     db.session.add(host)
    #
    # fabu = Host('JSSH2WEB16027', '预发布')
    # other = Host('JSSH2WEB16026', '其他')
    # db.session.add_all([fabu, other])
    # db.session.commit()


@manager.command
def initadmin():
    "Init admin Account"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if User.query.filter_by(user_name="admin").first() is None:
        admin = User("admin", "123456", "admin@local.com", "Admin", now)
        db.session.add(admin)
        db.session.commit()
    else:
        print("Admin Account is already existing")


if __name__ == '__main__':
    manager.run()
