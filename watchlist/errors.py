from watchlist import app
from watchlist.models import User
from flask import render_template


@app.errorhandler(404)
def not_found(e):
    user = User.query.first()
    return render_template('errors/404.html'),404
