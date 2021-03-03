import os
import datetime as dt
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # Set up app depending on if testing or not
    if test_config is None:
        setup_db(app)
    else:
        app.config['TESTING'] = True
        # Use the test database if testing
        setup_db(app, os.environ['TEST_DATABASE_URL'])
    CORS(app)

    @app.route('/')
    def index():
        """Welcome message for root url"""
        return jsonify({
            'message': 'Hi',
            'docs': 'https://github.com/borenx1/Udacity-FSND-Capstone'
        })

    @app.route('/actors')
    @requires_auth("view:actors")
    def get_actors():
        """GET "/actors" endpoint.

        Actor objects have members: `id`, `name`, `age`, `gender`.

        :returns: An array of all actors in JSON format.
        """
        actors = Actor.query.order_by(Actor.id).all()
        return jsonify([a.format() for a in actors])

    @app.route('/movies')
    @requires_auth("view:movies")
    def get_movies():
        """GET "/movies" endpoint.

        Movie objects have members: `id`, `title`, `release_date`. Member `release_date` has the format `yyyy-mm-dd`.

        :returns: An array of all movies in JSON format.
        """
        movies = Movie.query.order_by(Movie.id).all()
        return jsonify([m.format() for m in movies])

    @app.route('/actors', methods=['POST'])
    @requires_auth("add:actor")
    def post_actor():
        """POST "/actors" endpoint.

        Add a new actor. Receives a json object with the members: name, age, gender. Age must be a positive integer.

        :returns: A JSON object with the member `id`: the id of the newly created actor.
        :raises HTTPException: An appropriate HTTP exception.
        """
        data = request.get_json()
        if not data:
            abort(400)
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)
        # Raise bad request error if name or age data is not sent
        if name is None or age is None:
            abort(400)
        # Raise bad request error if age is not an integer
        if not isinstance(age, int):
            abort(400)
        # Raise unprocessable error if age is negative
        if age < 0:
            abort(422)
        # Raise unprocessable error if any error occurs during adding the new actor to the database
        try:
            new_actor = Actor(name, age, gender)
            new_actor.insert()
            return jsonify({
                'id': new_actor.id
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth("add:movie")
    def post_movie():
        """POST "/movies" endpoint.

        Add a new movie. Receives a json object with the members: title, release_date.

        :returns: A JSON object with the member `id`: the id of the newly created movie.
        :raises HTTPException: An appropriate HTTP exception.
        """
        data = request.get_json()
        if not data:
            abort(400)
        title = data.get('title', None)
        release_date = data.get('release_date', None)
        # Raise bad request error if title or release_date data is not sent
        if title is None or release_date is None:
            abort(400)
        # Raise unprocessable error if any error occurs during adding the new movie to the database
        try:
            # Convert date in "yyyy-mm-dd" format to a date object
            release_date = dt.date.fromisoformat(release_date)
            new_movie = Movie(title, release_date)
            new_movie.insert()
            return jsonify({
                'id': new_movie.id
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("update:actor")
    def patch_actor(actor_id):
        """PATCH "/actors/<actor-id>" endpoint.

        Updates at least one attribute: name, age, gender of the actor with the given id.

        :returns: A JSON object representing the updated actor with members: id, name, age, gender.
        :raises HTTPException: An appropriate HTTP exception.
        """
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        data = request.get_json()
        if not data:
            abort(400)
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)
        # Raise bad request error if all attributes are not given (must give at least one)
        if name is None and age is None and gender is None:
            abort(400)
        if age is not None:
            # Raise bad request error if age is not an integer
            if not isinstance(age, int):
                abort(400)
            # Raise unprocessable error if age is negative
            if age < 0:
                abort(422)
        # Raise unprocessable error if any error occurs during updating the actor
        try:
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender
            actor.update()
            return jsonify(actor.format())
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("update:movie")
    def patch_movie(movie_id):
        """PATCH "/movies/<movie-id>" endpoint.

        Updates at least one attribute: title, release_date of the movie with the given id.

        :returns: A JSON object representing the updated movie with members: id, title, release_date.
        :raises HTTPException: An appropriate HTTP exception.
        """
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
        data = request.get_json()
        if not data:
            abort(400)
        title = data.get('title', None)
        release_date = data.get('release_date', None)
        # Raise bad request error if all attributes are not given (must give at least one)
        if title is None and release_date is None:
            abort(400)
        # Raise unprocessable error if any error occurs during updating the actor
        try:
            if title is not None:
                movie.title = title
            if release_date is not None:
                # Convert date in "yyyy-mm-dd" format to a date object
                movie.release_date = dt.date.fromisoformat(release_date)
            movie.update()
            return jsonify(movie.format())
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actor(actor_id):
        """Delete "/actors/<actor-id>" endpoint.

        Delete the actor with the given id.

        :returns: The id of the deleted actor.
        :raises HTTPException: Raises 404 not found error if the actor does not exist.
        """
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify({'id': actor.id})
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movie(movie_id):
        """Delete "/movies/<movie-id>" endpoint.

        Delete the movie with the given id.

        :returns: The id of the deleted movie.
        :raises HTTPException: Raises 404 not found error if the movie does not exist.
        """
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({'id': movie.id})
        except Exception as e:
            print(e)
            abort(500)

    @app.errorhandler(400)
    def error_400(error):
        return jsonify({
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(401)
    def error_401(error):
        return jsonify({
            'error': 401,
            'message': 'unauthorized'
        }), 401

    @app.errorhandler(403)
    def error_403(error):
        return jsonify({
            'error': 403,
            'message': 'forbidden'
        }), 403

    @app.errorhandler(404)
    def error_404(error):
        return jsonify({
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(405)
    def error_405(error):
        return jsonify({
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def error_422(error):
        return jsonify({
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def error_500(error):
        return jsonify({
            'error': 500,
            'message': 'internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def error_auth(ex):
        """Error handler for `AuthError`. Status code is 401 or 403 depending on the error.
        The response message matches the exception error message.
        """
        return jsonify({
            'error': ex.status_code,
            'message': ex.error
        }), ex.status_code

    return app


if __name__ == '__main__':
    APP = create_app()
    APP.run(host='localhost', port=5000, debug=True)
