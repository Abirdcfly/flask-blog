# -*- coding:utf-8 -*-
from flask import render_template, session, redirect, url_for, flash, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm
from flask.ext.login import login_required


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/', methods=['GET', 'POST'])
def index():
    title = 'Home'
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['AWOTER_ADMIN']:
                send_email(current_app.config['AWOTER_ADMIN'], U'新用户加入',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        if session['known'] == False:
            flash(u'欢迎新成员')
        else:
            flash(u'欢迎回来')
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', title=title, form=form, name=session.get('name'),
                           known=session.get('known', False))


@main.route('/secret')
@login_required
def secret():
    return u'您必须登陆！'
