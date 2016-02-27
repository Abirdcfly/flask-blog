# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField(u'账号', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'提交')
