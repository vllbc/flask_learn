from app import app,db
from app.models import MovieModel,SayModel,UserModel
from flask import jsonify,request,abort


@app.route("/api/movies")
def getmovies():
    movies = MovieModel.query.all()
    lists = []
    for movie in movies:
        lists.append({
            'id': movie.id,
            'title': movie.title,
            'year': movie.year
        }
        )
    return jsonify(movies=lists)


@app.route("/api/movie/<int:movieid>")
def get_movie(movieid):
    movie = MovieModel.query.get_or_404(movieid)
    m = {
        'id': movieid,
        'title': movie.title,
        'year': movie.year
    }
    return jsonify(movie=m)


@app.route("/api/add_movie", methods=['POST'])
def add_movie():
    if not request.form or 'title' not in request.form:
        abort(404)
    movie = MovieModel(title=request.form['title'], year=request.form['year'])
    db.session.add(movie)
    db.session.commit()
    m = {
        'id': movie.id,
        'title': movie.title,
        'year': movie.year
    }
    return jsonify(movie=m), 201


@app.route("/api/update_movie/<int:movieid>",methods=['PUT'])
def update_movie(movieid):
    movie = MovieModel.query.get_or_404(movieid)
    movie.title = request.form['title']
    movie.year = request.form['year']
    db.session.commit()
    m = {
        'id': movieid,
        'title': movie.title,
        'year': movie.year
    }
    return jsonify(movie=m),201


@app.route("/api/delete_movie/<int:movieid>",methods=['delete'])
def delete_movie(movieid):
    movie = MovieModel.query.get_or_404(movieid)
    db.session.delete(movie)
    db.session.commit()
    movies = MovieModel.query.all()
    lists = []
    for movie in movies:
        lists.append({
            'id': movie.id,
            'title': movie.title,
            'year': movie.year
        }
        )
    return jsonify(movies=lists)
