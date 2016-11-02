#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/14

from flask_assets import Bundle

bundles = {
    'common_css': Bundle(
        'css/body.css',
        'css/lib/adminlte/adminlte.min.css',
        'css/lib/bootstrap/bootstrap.min.css',
        'css/lib/skins/skin-blue.min.css',
        'css/lib/fontawesome/font-awesome.min.css',
        output='css/common.css',
        filters='cssmin'
    ),
    'common_js': Bundle(
        'js/lib/jquery/jquery.min.js',
        'js/lib/app/app.min.js',
        'js/lib/bootstrap/bootstrap.min.js',
        'js/lib/validate/jquery.validate.js',
        output='js/common.js',
        filters='jsmin'
    ),

}
