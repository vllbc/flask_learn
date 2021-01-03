from flask import Flask,url_for,escape


app = Flask(__name__)


@app.route("/")
def hello():
    return 'hello world! <img src="http://helloflask.com/totoro.gif">'

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