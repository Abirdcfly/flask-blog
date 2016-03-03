# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required,  current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ChangeEmailForm
from .. import db
from ..email import send_email


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
    title = u'注册'
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, u'WOTER注册确认', 'auth/email/confirm', user=user, token=token)
        flash(u'确认邮件已发送，请查收！')
        # return redirect(url_for('auth.login'))
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form, title=title)





@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u'此邮箱已确认，THX')
    else:
        flash(u'确认链接已失效')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    title = u'请确认账户'
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html', title=title)


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, u'WOTER注册确认', 'auth/email/confirm', user=current_user, token=token)
    flash(u'一封新的确认邮件已发送，请查收！')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    title = u'修改密码'
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash(u'您的密码已修改，请牢记新密码！')
        return redirect(url_for('main.index'))
    return render_template('auth/change-password.html', title=title, form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email():
    title = u'修改邮箱'
    form = ChangeEmailForm()
    if current_user.confirmed == True:
        if form.validate_on_submit():
            current_user.email = form.email.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'您的邮箱地址已修改，请牢记！')
            return redirect(url_for('main.index'))
    else:
        flash(u'请先确认您的原邮箱地址！')
        return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/change-email.html', title=title, form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))
