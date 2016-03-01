# -*- coding:utf-8 -*-
from flask import render_template, session, redirect, url_for, flash, current_app, request
from .. import db
from ..models import User, Role, Permission, Post
from ..email import send_email
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm
from flask.ext.login import login_required, current_user
from flask import abort
from ..decorators import admin_required


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

#
# @main.route('/secret')
# @login_required
# def secret():
#     return u'您必须登陆！'


@main.route('/user/<username>')
def user_page(username):
    user = User.query.filter_by(username=username).first_or_404()
    title = str(user.username)
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['AWOTER_DOC_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, title=title, posts=posts, pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    title = u'修改个人信息'
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'您的修改已经保存')
        return redirect(url_for('.user_page', username=current_user.username))
    form.nickname.data = current_user.nickname
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit-profile.html', title=title, form=form, username=current_user.username)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.nickname = form.nickname.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash(u'数据已经更新！')
        return redirect(url_for('.user_page', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.nickname.data = user.nickname
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit-profile.html', form=form, user=user)


@main.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    title = u'编辑文章'
    form = PostForm()
    if form.validate_on_submit():
                    # current_user.can(Permission.WRITE_ARTICLES) and \

        posts = Post(article_title=form.article_title.data,
                     body=form.body.data,
                     author=current_user._get_current_object())
        db.session.add(posts)
        flash(u'已提交！')
        return redirect(url_for('.doc'))
    return render_template('post.html', title=title, form=form)


@main.route('/doc')
def doc():
    title = u'文章列表'
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['AWOTER_DOC_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('doc.html', title=title, posts=posts, pagination=pagination)


@main.route('/res-mods')
def res_mods():
    title = u'插件'
    return render_template('res-mods.html', title=title)


@main.route('/hd')
def hd():
    title = u'最新活动'
    return render_template('hd.html', title=title)


@main.route('/video')
def video():
    title = u'视频'
    return render_template('video.html', title=title)