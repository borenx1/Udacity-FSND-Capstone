import os
import datetime as dt
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def setup_db(app, database_path=None):
    """Binds a flask application and a SQLAlchemy service."""
    # Set the default database path to the environment variable DATABASE_URL
    if database_path is None:
        database_path = os.environ['DATABASE_URL']
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    app.db = db
    db.init_app(app)


class Movie(db.Model):
    """SQLAlchemy model for a movie.
    """
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=200), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __init__(self, title=None, release_date=None):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f'<Movie id:{self.id} title:{self.title} release:{self.release_date}>'

    def format(self):
        """Returns a dictionary with key:value pairs of this object: id, title, release_date.
        The value release_date is a string with the format "yyyy-mm-dd".
        """
        if isinstance(self.release_date, (dt.date, dt.datetime)):
            json_release_date = self.release_date.strftime('%Y-%m-%d')
        else:
            json_release_date = self.release_date
        return {
            'id': self.id,
            'title': self.title,
            'release_date': json_release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    """SQLAlchemy model for an actor.
    """
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=200), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(length=100), nullable=True)

    def __init__(self, name=None, age=None, gender=None):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f'<Actor id:{self.id} name{self.name} age:{self.age} gender:{self.gender}>'

    def format(self):
        """Returns a dictionary with key:value pairs of this object: id, name, age, gender."""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
