from flask import Flask
from flask.cli import load_dotenv
from flask_smorest import Api
from db import db
import models
from resources.user import blp as UserBlueprint
from resources.habit import blp as HabitBlueprint
from resources.complete_habits import blp as CompleteHabitsBlueprint
from flask_jwt_extended import JWTManager
import os
import dotenv
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['API_TITLE'] = "Habit Tracker"
    app.config['API_VERSION'] = '1.0.0'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    Migrate(app, db, render_as_batch=True)
    api = Api(app)

    JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(HabitBlueprint)
    api.register_blueprint(CompleteHabitsBlueprint)

    return app

create_app()