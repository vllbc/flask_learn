from watchlist import app,db
from watchlist.models import Movie,User
from flask import flash,request,redirect,url_for,render_template
from flask_login import current_user,login_required,logout_user,login_user



@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for("index"))
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
@login_required
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


@app.route("/settings",methods=['GET','POST'])
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash("Invaild input")
            return redirect(url_for("settings"))
        current_user.name = name
        db.session.commit()
        flash("Settings update")
        return redirect(url_for("index"))
    return render_template("settings.html")



@app.route("/movie/delete/<int:movie_id>",methods=['GET','POST'])
@login_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item deleted")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')




@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页