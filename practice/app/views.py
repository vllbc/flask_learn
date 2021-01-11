from app import app, db, bootstrap

from flask import render_template, request, redirect, url_for, flash
from app.forms import NewSay, editsay, NewMovie,EditMovie


@app.route("/", methods=['GET', 'POST'])
def index():
    from app.models import MovieModel
    form = NewMovie()
    if form.validate_on_submit():
        data = request.form
        if len(data['title']) > 20  or len(data['year']) != 4:
            return redirect(url_for("index"))
        new_movie = MovieModel(title=data['title'],year=data['year'])
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('index'))
    movies = MovieModel.query.all()
    return render_template("index.html", movies=movies, form=form)


@app.route("/editmovie/<int:movieid>", methods=['GET', 'POST'])
def editmovie(movieid):
    from app.models import MovieModel
    form = EditMovie()
    if form.validate_on_submit():
        movie = MovieModel.query.get_or_404(movieid)
        data = request.form
        movie.title = data['title']
        movie.year = data['year']
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", bootstrap=bootstrap, form=form)


@app.route('/deletemovie/<int:movieid>')
def deletemovie(movieid):
    from app.models import MovieModel
    movie = MovieModel.query.get_or_404(movieid)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/comments", methods=['GET', 'POST'])
def comments():
    from app.models import SayModel
    form = NewSay()
    if form.validate_on_submit():
        data = request.form
        say = SayModel(name=data['name'], body=data['body'])
        db.session.add(say)
        db.session.commit()
        return redirect(url_for("comments"))
    says = SayModel.query.order_by(SayModel.timestamp.desc()).all()
    return render_template("comments.html", says=says, form=form, bootstrap=bootstrap)


@app.route("/delete/<int:sayid>", methods=['GET', 'POST'])
def delete_comments(sayid):
    from app.models import SayModel
    say = SayModel.query.get_or_404(sayid)
    db.session.delete(say)
    db.session.commit()
    return redirect(url_for("comments"))


@app.route('/edit/<int:sayid>', methods=['GET', 'POST'])
def edit_comments(sayid):
    from app.models import SayModel
    form = editsay()
    if form.validate_on_submit():
        data = request.form
        say = SayModel.query.get_or_404(sayid)
        say.name = data['name']
        say.body = data['body']
        db.session.commit()
        return redirect(url_for("comments"))
    return render_template("edit.html", form=form, bootstrap=bootstrap)
