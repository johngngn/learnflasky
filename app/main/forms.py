#-*- coding:utf8 -*-
#coding=utf-8
from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role, User
from wtforms import ValidationError


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('submit')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Email(), Length(1, 64)])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Username must have only letters, '
                                          'numbers, dots or underscores.')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        print(self.role.choices)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        print(Role.query.order_by(Role.name).all())
        print(self.role.choices)
        self.user = user

    #以下构造函数会自动验证表单
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')