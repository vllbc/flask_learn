from app import app, db, bootstrap

from flask import render_template, request, redirect, url_for, flash
from app.forms import newsay, editsay


@app.route("/", methods=['GET', 'POST'])
def index():
    from app.models import SayModel
    form = newsay()
    if form.validate_on_submit():
        data = request.form
        if len(data['name']) > 20 or len(data['body']) > 200:
            flash("error！")
            return redirect(url_for("index"))
        say = SayModel(name=data['name'], body=data['body'])
        db.session.add(say)
        db.session.commit()
        return redirect(url_for("index"))
    says = SayModel.query.all()
    return render_template("index.html", says=says, form=form, bootstrap=bootstrap)


@app.route("/delete/<int:sayid>", methods=['GET', 'POST'])
def delete(sayid):
    from app.models import SayModel
    say = SayModel.query.get_or_404(sayid)
    db.session.delete(say)
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/edit/<int:sayid>', methods=['GET', 'POST'])
def edit(sayid):
    from app.models import SayModel
    form = editsay()
    if form.validate_on_submit():
        data = request.form
        say = SayModel.query.get_or_404(sayid)
        say.name = data['name']
        say.body = data['body']
        db.session.commit()
        flash("edit ok")
        return redirect(url_for("index"))
    return render_template("edit.html", form=form, bootstrap=bootstrap)
