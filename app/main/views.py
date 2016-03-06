# -*- coding:utf-8 -*-
from flask import render_template, session, redirect, url_for, \
    flash, current_app, request, make_response
from .. import db
from ..models import User, Role, Permission, Post, Comment
from ..email import send_email
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, CkeditorPostForm, CommentForm, MarkdownPostForm
from flask.ext.login import login_required, current_user
from flask import abort
from ..decorators import admin_required, permission_required


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/index')
@main.route('/', methods=['GET', 'POST'])
def index():
    # try:
    #     db.create_all()
    # except:
    #     pass
    title = 'Home'
    # form = NameForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         session['known'] = False
    #         if current_app.config['WOTER_ADMIN']:
    #             send_email(current_app.config['WOTER_ADMIN'], U'新用户加入',
    #                        'mail/new_user', user=user)
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     if session['known'] == False:
    #         flash(u'欢迎新成员')
    #     else:
    #         flash(u'欢迎回来')
    #     form.name.data = ''
    #     return redirect(url_for('.index'))
    return render_template('index.html', title=title)
    # , form=form, name=session.get('name'), known=session.get('known', False))


@main.route('/user/<username>')
def user_page(username):
    detail_show = False
    user = User.query.filter_by(username=username).first_or_404()
    title = str(user.username)
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['WOTER_DOC_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, title=title,
                           posts=posts, pagination=pagination, detail_show=detail_show)


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

# 现在不能用。待我哪天细查代码
# flask_wysiwyg
# @main.route('/post', methods=['GET', 'POST'])
# @login_required
# def post():
#     title = u'编辑文章'
#     form = PostForm()
#     if current_user.can(Permission.WRITE_ARTICLES) and \
#             form.validate_on_submit():
#         posts = Post(article_title=form.article_title.data,
#                      body=form.body.data,
#                      author=current_user._get_current_object())
#         db.session.add(posts)
#         flash(u'已提交！')
#         return redirect(url_for('.doc'))
#     # return render_template('post.html', title=title, form=form)
#     return render_template('post-rich-text-edit.html', title=title, form=form)


@main.route('/doc')
def doc():
    title = u'文章列表'
    detail_show = False
    show_follwed = False
    if current_user.is_authenticated:
        show_follwed = bool(request.cookies.get('show_followed', ''))
    if show_follwed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['WOTER_DOC_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('doc.html', title=title, posts=posts,
                           pagination=pagination, detail_show=detail_show, show_follwed=show_follwed)


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


@main.route('/doc/<int:id>', methods=['GET', 'POST'])
def doc_detail(id):
    post = Post.query.get_or_404(id)
    title = post.article_title
    detail_show = True
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        flash(u'你的评论已提交！')
        return redirect(url_for('main.doc_detail', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
            current_app.config['WOTER_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['WOTER_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('doc.html', title=title, posts=[post], detail_show=detail_show,
                           form=form, comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_doc(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = MarkdownPostForm()
    if form.validate_on_submit():
        post.article_title = form.article_title.data
        post.body = form.body.data
        db.session.add(post)
        flash(u'修改已保存')
        return redirect(url_for('main.doc', id=post.id,
                                title=post.article_title, posts=[post], detail_show=True))
    form.article_title.data = post.article_title
    form.body.data = post.body
    return render_template('post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'非法用户！')
        return redirect(url_for('main.index'))
    if current_user.is_following(user):
        flash(u'你已经关注了他')
        return redirect(url_for('main.user_page', username=username))
    current_user.follow(user)
    flash(u'你关注了 %s.' % username)
    return redirect(url_for('main.user_page', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'非法用户！')
        return redirect(url_for('main.index'))
    if not current_user.is_following(user):
        flash(u'你没有关注他！')
        return redirect(url_for('main.user_page', username=username))
    current_user.unfollow(user)
    flash(u'你不再关注 %s ' % username)
    return redirect(url_for('main.user_page', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'非法用户！')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['WOTER_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"关注者列表",
                           endpoint='main.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'非法用户！')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['WOTER_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"他关注的人",
                           endpoint='main.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('main.doc')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('main.doc')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    title = u'管理评论'
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['WOTER_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments, title=title,
                           page=page, pagination=pagination)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


# Flask-CKEditor可用。图片，文件上传无效。
# https://github.com/neo1218/flask-ckeditor
@main.route('/cpost', methods=['GET', 'POST'])
@login_required
def ckeditor_post():
    title = u'编辑文章'
    form = CkeditorPostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        posts = Post(article_title=form.article_title.data,
                     body=form.body.data,
                     author=current_user._get_current_object())
        db.session.add(posts)
        flash(u'已提交！')
        return redirect(url_for('.doc'))
    return render_template('post-ckeditor.html', title=title, form=form)


@main.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """file/img upload interface"""
    form = CkeditorPostForm()
    # response = form.upload(endpoint=app)
    # return response
    form.upload(endpoint=main)


@main.route('/mpost', methods=['GET', 'POST'])
@login_required
def markdown_post():
    title = u'编辑文章'
    form = MarkdownPostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        posts = Post(article_title=form.article_title.data,
                     body=form.body.data,
                     author=current_user._get_current_object())
        db.session.add(posts)
        flash(u'已提交！')
        return redirect(url_for('.doc'))
    return render_template('post.html', title=title, form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

# 存入数据库，可以用= = 然而我的读取还有问题。
# @main.route('/upload', methods=['GET', 'POST'])
# def upload_avatar():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             current_user.avatar_local = file.read()
#             db.session.add(current_user)
#             db.session.commit()
#             return redirect(url_for('main.user_page', username=current_user.username))
#     return render_template('upload_avatar.html', user=current_user)


# 存储头像到SAE storage
from sae.storage import Bucket
bucket = Bucket('avatar')


@main.route('/upload', methods=['GET', 'POST'])
def upload_avatar():
    global aurl
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            files = file.read()
            bucket.put_object(file.filename, files)
            url = str(bucket.generate_url(file.filename))
            current_user.avatar_local_url = url
            db.session.add(current_user)
            db.session.commit()
            flash(u"头像已修改！")
            return current_user.gravatar
            # return redirect(url_for('main.user_page', username=current_user.username))
    return render_template('upload_avatar.html', user=current_user)
