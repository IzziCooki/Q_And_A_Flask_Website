import click
from flask.cli import with_appcontext

from .extensions import db
from .models import User, Question

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()
    user = User(name="izzi", unhashed_password="12345678", expert=True)
    db.session.add(user)
    
    question = Question(question="test", asked_by_id=1, expert_id=1)
    db.session.add(question)
    db.session.commit()
    
  
