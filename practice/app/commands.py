import click

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

    for i in range(count):
        say = SayModel(name=faker.name(),body=faker.sentence(),timestamp=faker.date_time_this_year())
        db.session.add(say)
    db.session.commit()
    click.echo("ALL WORKS OK!")
