# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp


class NameForm(Form):
    name = StringField(u'账号', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'提交')


class EditProfileForm(Form):
    nickname = StringField(u'昵称', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z0-9_]*$', 0, u'用户名只能包含大小写字母数字和下划线')])
    confirmed = BooleanField(u'已验证')
    role = SelectField(u'用户级别', coerce=int)
    nickname = StringField(u'昵称', validators=[Length(0, 64)])
    location = StringField(u'位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'确定修改')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm,self).__init__(*args, **kwargs)
        self.role.choices =[(role.id, role.name)for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'email地址已经注册！')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'此用户名已注册！')

