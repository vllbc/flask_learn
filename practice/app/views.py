from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, login_user, logout_user

from app import app, db
from app.forms import NewSay, editsay, NewMovie, EditMovie, LoginForm, SettingForm
from app.models import MovieModel, SayModel, UserModel


@app.route("/", methods=['GET', 'POST'])
def index():
    form = NewMovie()
    if form.validate_on_submit():
        data = request.form
        if len(data['title']) > 20 or len(data['year']) != 4:
            flash("格式不对！")
            return redirect(url_for("index"))
        new_movie = MovieModel(title=data['title'], year=data['year'])
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('index'))
    movies = MovieModel.query.all()
    return render_template("index.html", movies=movies, form=form)


@app.route("/editmovie/<int:movieid>", methods=['GET', 'POST'])
@login_required
def editmovie(movieid):
    form = EditMovie()
    if form.validate_on_submit():
        movie = MovieModel.query.get_or_404(movieid)
        data = request.form
        if len(data['title']) > 20 or len(data['year']) != 4:
            flash("格式不对！")
            return redirect(url_for("editmovie", movieid=movieid))
        movie.title = data['title']
        movie.year = data['year']
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", form=form)


@app.route('/deletemovie/<int:movieid>')
@login_required
def deletemovie(movieid):
    movie = MovieModel.query.get_or_404(movieid)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/comments", methods=['GET', 'POST'])
def comments():
    form = NewSay()
    if form.validate_on_submit():
        data = request.form
        say = SayModel(name=data['name'], body=data['body'])
        db.session.add(say)
        db.session.commit()
        return redirect(url_for("comments"))
    says = SayModel.query.order_by(SayModel.timestamp.desc()).all()
    return render_template("comments.html", says=says, form=form)


@app.route("/delete/<int:sayid>", methods=['GET', 'POST'])
@login_required
def delete_comments(sayid):
    say = SayModel.query.get_or_404(sayid)
    db.session.delete(say)
    db.session.commit()
    return redirect(url_for("comments"))


@app.route('/edit/<int:sayid>', methods=['GET', 'POST'])
@login_required
def edit_comments(sayid):
    form = editsay()
    if form.validate_on_submit():
        data = request.form
        say = SayModel.query.get_or_404(sayid)
        say.name = data['name']
        say.body = data['body']
        db.session.commit()
        return redirect(url_for("comments"))
    return render_template("edit.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = request.form
        username = data['username']
        password = data['password']
        user = UserModel.query.first()
        if user.username == username and user.validate_password(password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/setting", methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        user = UserModel.query.first()
        username = request.form['username']
        if len(username) > 20:
            flash("用户名过长！")
            return redirect(url_for("settings"))
        user.username = username
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("setting.html", form=form)


