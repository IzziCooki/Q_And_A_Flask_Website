from flask import Flask 

from .commands import create_tables
from .extensions import db, login_manager
from .models import User
from .routes.auth import auth
from .routes.main import main

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"]="dslhfjkshdlfjsvnksdjfnsf"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dbsvretlwljtwh:45879767620cde7aa549b5fdf0985a22f8bf59ae94b861a6d914f39ecd4d034a@ec2-54-163-254-204.compute-1.amazonaws.com:5432/d98q49rbnjpd4"

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    app.cli.add_command(create_tables)

    return app
