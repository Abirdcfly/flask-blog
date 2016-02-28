# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z0-9_]*$', 0, u'用户名只能包含大小写字母数字和下划线')])
    password = PasswordField(u'密码', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z0-9_]*$', 0, u'密码只能包含大小写字母数字和下划线')])
    password2 = PasswordField(u'确认密码', validators=[Required(), EqualTo('password', message=u'两次密码需要一致')])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'此邮箱已注册！')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'此用户名已注册！')


class ChangePasswordForm(Form):
    password = PasswordField(u'新密码', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z0-9_]*$', 0, u'密码只能包含大小写字母数字和下划线')])
    password2 = PasswordField(u'确认密码', validators=[Required(), EqualTo('password', message=u'两次密码需要一致')])
    submit = SubmitField(u'确定')


class ChangeEmailForm(Form):
    email = StringField(u'新邮箱', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField(u'确定')