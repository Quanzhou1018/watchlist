# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

#通过实例化Flask类，创建一个程序对象app
app = Flask(__name__)

#通过Flask.config字典这一统一来写入和获取这些配置变量（一般放到扩展类实例化语句之前）
#flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。
# session 用来在请求间存储数据，它会把数据签名后存储到浏览器的 Cookie 中
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev') # 等同于 app.secret_key = 'dev'
#下面写入了一个 SQLALCHEMY_DATABASE_URI 变量来告诉 SQLAlchemy 数据库连接地址
#app.root_path 返回程序实例所在模块的路径（目前来说，即项目根目录），我们使用它来构建文件路径
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #关闭对模型修改的监控

#初始化扩展，传入程序实例app
db = SQLAlchemy(app)#使用SQLAlchemy

login_manager = LoginManager(app)#使用LoginManager

#填入 app.route() 装饰器的第一个参数是 URL 规则字符串
#注册处理函数，也就是给这个函数带上一个装饰器帽子

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User# 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的主键查询对应的用户
    return user # 返回用户对象

#未登录时如果访问（/movie/edit/..），则会导向到登陆界面
login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'

#模板上下文处理函数（对于多个模板内部都需要使用的变量推荐采用）
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands