# -*- coding:utf-8 -*-
from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    title = u'404 无法找到网页'
    return render_template('404.html', title=title), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    title = u'500 内部错误'
    return render_template('500.html', title=title), 500


@main.app_errorhandler(403)
def forbidden(e):
    title = u'403 权限错误！'
    return render_template('403.html', title=title), 403

