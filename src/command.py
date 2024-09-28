import click
from flask import Blueprint

from app.db import db
from models.user import User

cmd = Blueprint('cmd', __name__)


@cmd.cli.command("create-super-user")
@click.argument("email")
@click.argument("password")
def create_user(email, password):
    user = User('Admin', 'Admin', 'Admin', '999111222', password, email, 'Admin')
    user.is_admin = True
    db.session.add(user)
    db.session.commit()
    click.echo(f'User {email} has been created')


@cmd.cli.command("create-all-table")
def create_all_table():
    db.create_all()
    click.echo('DB CREATED')


