from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控


db = SQLAlchemy(app)

login_manager  = LoginManager(app)


@login_manager.user_loader
def load_user(userid):
    from watchlist.models import User
    user = User.query.get(int(userid))
    return user


login_manager.login_view = 'login'



@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

from watchlist import view, errors, commands
