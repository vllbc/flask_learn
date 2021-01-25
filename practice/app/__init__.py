from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
moment = Moment(app)
bootstrap = Bootstrap(app)

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    from app.models import UserModel
    user = UserModel.query.get(int(userid))
    return user


@app.context_processor
def inject_user():
    from app.models import UserModel
    user = UserModel.query.first()
    return dict(user=user)


from app import views, commands, errors
from app.api import api_function

