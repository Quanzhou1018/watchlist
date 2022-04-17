import os
import sys
import click

from flask import escape,Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 在扩展类实例化前加载配置
db=SQLAlchemy(app)

name = 'Quanzhou Xiang'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)   #主键
    name=db.Column(db.String(20))   #名字

class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60))
    year=db.Column(db.String(4))

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', name=name, movies=movies)


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html', user=user), 404  # 返回模板和状态码


