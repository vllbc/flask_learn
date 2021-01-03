from flask import Flask,url_for,escape,render_template


app = Flask(__name__)


@app.route("/")
def hello():
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
    return render_template("index.html",name='wlb',movies=movies)

@app.route('/user/<name>')
def user(name):
    return f"<h1>HELLO {escape(name)}!</h1>"


@app.route('/test')
def test_for_user():
    print(url_for("hello"))
    print(url_for('user',name='wlb'))
    print(url_for("test_for_user"))
    return 'Testpage'
app.run()