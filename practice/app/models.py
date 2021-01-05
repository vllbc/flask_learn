from re import T
from app.views import index
from werkzeug.exceptions import default_exceptions
from app import db
from datetime import date, datetime



class SayModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)

    