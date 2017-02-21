#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/11


import datetime
import os

from flask_script import Manager


from app import create_app, db
from app.models import User

app = create_app(os.environ.get('FLASK_ENV') or 'dev')
manager = Manager(app)


@manager.command
def createdb():
    "Create DataBase Tables"
    db.create_all()


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