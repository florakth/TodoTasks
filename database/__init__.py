
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is not None:
        app.config.from_pyfile(config_name)

    db.init_app(app)
    with app.app_context():

        from .model import TodoTasks
        db.create_all()
    return app



