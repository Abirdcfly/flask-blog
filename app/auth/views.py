# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = u'登陆'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误！')
    return render_template('auth/login.html', title=title, form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已退出登录！')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.username.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        flash(u'你已注册成功！')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)