from app import app
from flask import render_template

@app.errorhandler(404)
def error404():
    return render_template('errors/404.html'),404
