from app import app,db

from flask import render_template,request,redirect,url_for


@app.route("/",methods=['GET','POST'])
def index():
    from app.models import SayModel
    if request.method == 'POST':
        data = request.form
        say = SayModel(name=data['name'],body=data['body'])
        db.session.add(say)
        db.session.commit()
        return redirect(url_for("index"))
    says = SayModel.query.all()    
    return render_template("index.html",says=says)


