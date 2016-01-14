#-*- coding:utf8 -*-
#coding=utf-8
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown
from config import config
from flask.ext.mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()
toolbar = DebugToolbarExtension()
login_manage = LoginManager()
login_manage.session_protection = 'strong'
login_manage.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    ''' config 是一个字典, 对不同的继承于Config的类进行别名映射, 仔细看定义就可以知道.

        config[config_name]就是根据某个名称获取某个类, 也就是字典取值.

        字典取值出来之后就是一个类, 那个类有个静态方法init_app, 这个可以从Config的定义看出来. 当然这个方法什么也没有做, 是为了方便扩展, 其他的类这个方法是有定义的, 可以看看.
    '''
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    toolbar.init_app(app)
    login_manage.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app