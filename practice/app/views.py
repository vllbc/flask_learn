from app import app,db

from flask import render_template,request


@app.route("/")
def index():
    from app.models import SayModel
    says = SayModel.query.all()    
    return render_template("index.html",says=says)
