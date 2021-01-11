import click
from app.models import MovieModel
from app import db,app
from app.models import SayModel


@app.cli.command()
@click.option("--drop",is_flag=True)
def initdb(drop):
    if drop:
        db.drop_all()
        click.echo("Drop tables")
    db.create_all()
    click.echo("WORKS OK!")


@app.cli.command()
@click.option("--count",default=20)
def forge(count):
    from faker import Faker
    db.drop_all()
    db.create_all()
    
    faker = Faker()
    click.echo("WORKING...")

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
    for m in movies:
        movie = MovieModel(title=m['title'], year=m['year'])
        db.session.add(movie)
    for i in range(count):
        say = SayModel(name=faker.name(),body=faker.sentence(),timestamp=faker.date_time_this_year())
        db.session.add(say)
    db.session.commit()
    click.echo("ALL WORKS OK!")
