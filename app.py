import re
from flask import Flask, cli,url_for,escape,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import os
import click

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控


db = SQLAlchemy(app)

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
@click.option("--drop",is_flag=True,help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("ALL WORKS OK!")

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)



@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        title = request.form.get("title")
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) >60:
            flash("Invalid input!")
            return redirect(url_for("index"))
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash("Item created")
        return redirect(url_for("index"))

    movies = Movie.query.all()
    return render_template("index.html",movies=movies)



@app.route("/movie/edit/<int:movie_id>",methods=['GET','POST'])
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit_movie', movie_id=movie_id))
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie=movie) 

@app.route("/movie/delete/<int:movie_id>",methods=['GET','POST'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item deleted")
    return redirect(url_for('index'))
@app.errorhandler(404)
def not_found(e):
    user = User.query.first()
    return render_template('404.html'),404
if __name__ == "__main__":
    app.run()